from django.shortcuts import render
import yfinance as yf
from statsmodels.tsa.stattools import adfuller
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .forms import CointegrationForm

def calculate_cointegration(request):
    result = None
    backtest_result = None
    close_prices = None
    significance = None

    if request.method == 'POST':
        form = CointegrationForm(request.POST)
        if form.is_valid():
            ticker_1 = form.cleaned_data['ticker_1']
            ticker_2 = form.cleaned_data['ticker_2']
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']

            # Data Collection
            tickers = [ticker_1, ticker_2]
            data = yf.download(tickers, start=start_date, end=end_date)

            if 'Close' in data:
                close_prices = data['Close']
                try:
                    X = close_prices[ticker_2].values.reshape(-1, 1)
                    y = close_prices[ticker_1].values

                    model = LinearRegression().fit(X, y)
                    beta = model.coef_[0]
                    alpha = model.intercept_
                    close_prices['Spread'] = y - (beta * X.squeeze() + alpha)

                    adf_result = adfuller(close_prices['Spread'])
                    
                    if adf_result[0] <= adf_result[4]['1%']:
                        significance = "Statistically significant and stationary at 1%"
                    elif adf_result[0] <= adf_result[4]['5%']:
                        significance = "Statistically significant and stationary at 5%"
                    elif adf_result[0] <= adf_result[4]['10%']:
                        significance = "Statistically significant and stationary at 10%"
                    else:
                        significance = "Not statistically significant below 10%"

                    result = {
                        'adf_statistic': adf_result[0],
                        'p_value': adf_result[1],
                        'critical_values': adf_result[4],
                        'significance': significance,
                    }

                    # Handle backtesting if button pressed
                    if 'backtest' in request.POST:
                        print("BACKTESTING")
                        
                        backtest_result = grid_search(close_prices, tickers)

                except Exception as e:
                    result = {'error': f"Error in analysis: {e}"}
    else:
        form = CointegrationForm()

    return render(
        request,
        'analysis/calculate.html',
        {
            'form': form,
            'result': result,
            'backtest_result': backtest_result,
        },
    )


def backtest_strategy(close_prices, tickers, entry_threshold, exit_threshold):
    data = close_prices.copy()
    data['mean'] = data['Spread'].mean()
    data['std'] = np.std(data['Spread'])

    def calculate_zscore(series):
        return (series - series.mean()) / np.std(series)
    data['Z-Score'] = calculate_zscore(data['Spread'])

    data[f'Long_{tickers[0]}'] = 0
    data[f'Short_{tickers[1]}'] = 0

    print(data)

    for i in range(len(data)):
        if data['Z-Score'].iloc[i] > entry_threshold:
            data.at[data.index[i], f'Long_{tickers[0]}'] = -1
            data.at[data.index[i], f'Short_{tickers[1]}'] = 1
        elif data['Z-Score'].iloc[i] < -entry_threshold:
            data.at[data.index[i], f'Long_{tickers[0]}'] = 1
            data.at[data.index[i], f'Short_{tickers[1]}'] = -1
        elif abs(data['Z-Score'].iloc[i]) < exit_threshold:
            data.at[data.index[i], f'Long_{tickers[0]}'] = 0
            data.at[data.index[i], f'Short_{tickers[1]}'] = 0
        else:
            if i > 0:
                data.at[data.index[i], f'Long_{tickers[0]}'] = data.at[data.index[i-1], f'Long_{tickers[0]}']
                data.at[data.index[i], f'Short_{tickers[1]}'] = data.at[data.index[i-1], f'Short_{tickers[1]}']

    # Calculate Strategy Returns
    data[f'{tickers[0]}_Returns'] = data[tickers[0]].pct_change()
    data[f'{tickers[1]}_Returns'] = data[tickers[1]].pct_change()
    data['Strategy_Returns'] = (
        data[f'Long_{tickers[0]}'] * data[f'{tickers[0]}_Returns']
        + data[f'Short_{tickers[1]}'] * data[f'{tickers[1]}_Returns']
    )
    data['Cumulative_Strategy_Returns'] = (1 + data['Strategy_Returns']).cumprod()

    # Performance Metrics
    annualized_return = data['Strategy_Returns'].mean() * 252
    print(annualized_return)
    annualized_volatility = data['Strategy_Returns'].std() * np.sqrt(252)
    print(annualized_volatility)
    sharpe_ratio = (
        (annualized_return - 0.05 ) / annualized_volatility
        if annualized_volatility != 0
        else np.nan
    )
    max_drawdown = (
        (data['Cumulative_Strategy_Returns'].cummax() - data['Cumulative_Strategy_Returns'])
        / data['Cumulative_Strategy_Returns'].cummax()
    ).min()

    print(data)

    return {
        'annualized_return': annualized_return,
        'annualized_volatility': annualized_volatility,
        'sharpe_ratio': sharpe_ratio,
        'max_drawdown': max_drawdown,
        'entry_threshold': entry_threshold,
        'exit_threshold': exit_threshold

    }





def grid_search(close_prices, tickers):

    entry_thresholds = np.arange(1.0, 4.1, 0.1) 
    exit_thresholds = np.arange(-1.1, 2.1, 0.1)

    # entry_thresholds = np.arange(1, 1.5, 0.1) 
    # exit_thresholds = np.arange(1, 1.5, 0.1)
 
    results = []
    
    for entry_threshold in entry_thresholds:
        for exit_threshold in exit_thresholds:
            if exit_threshold >= entry_threshold:
                continue
            performance = backtest_strategy(close_prices, tickers, entry_threshold, exit_threshold)
            results.append(performance)
    
    # Convert results to DataFrame
    results_df = pd.DataFrame(results)

    print("FINAL RESULTS DF //////////////// WE MADE IT TO THE END!")
    print(results_df)

    # 5. Identify Optimal Thresholds
    results_df = results_df.dropna()
    
    optimal_results = results_df.sort_values(
        by=['sharpe_ratio', 'annualized_return', 'max_drawdown'],
        ascending=[False, False, True]
    ).reset_index(drop=True)
    
    print("\nTop 5 Optimal Threshold Combinations:")
    print(optimal_results.head())

    best_entry = optimal_results.loc[0, 'entry_threshold']
    best_exit = optimal_results.loc[0, 'exit_threshold']
    
    print(f"\nBest Entry Threshold: {best_entry}")
    print(f"Best Exit Threshold: {best_exit}")

    return {
        'annualized_return1': optimal_results.loc[0, 'annualized_return'] * 100
    }