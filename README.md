# Statistical Arbitrage - Stock Pair Trading Analysis.

This project is a **stock pair trading analysis tool** that uses **linear regression** to model the relationship between two stock prices and calculate the **spread** between them. The spread is analyzed for **cointegration** to identify potential trading opportunities in a pairs trading strategy, which can then be backtested to caculate optimal entry and exit thresholds.

## Key Features

- **Linear Regression Modeling**  
  - Calculates the slope (`beta`) and intercept (`alpha`) of the relationship between two stocks' prices.
  - Computes the spread as the difference between the observed price and the mean price.

- **Cointegration Testing**  
  - Tests whether the spread between the two stocks is stationary (mean-reverting), a key requirement for pairs trading.

- **Visualization and Insights**  
  - Generates visualizations to analyze the spread and monitor its behavior over time.

## Planned Enhancements

1. **Model Transaction Costs**  
   - Incorporate transaction costs (e.g., brokerage fees, slippage) into the model to evaluate the net profitability of a trading strategy.

2. **Higher-Frequency Data**  
   - Replace daily stock prices with intraday or higher-frequency data to increase the number of data points and improve model precision.

3. **Dynamic Spread Thresholds**  
   - Develop adaptive thresholds for trading signals based on recent spread volatility.

4. **Deployment on Vercel**  
   - Plan to deploy the project as a web application using [Vercel](https://vercel.com), allowing users to:
     - Select stock pairs.
     - Perform backtesting with configurable parameters.

## Deployment

This project will be live on Vercel soon! Stay tuned for the deployment URL, which will be updated here.  

**Visit the web app:** [COMING SOON]

## How to Use the Code Locally

1. Clone the repository:  
   ```bash
   git clone https://github.com/Dev-0S/StatisticalArbitrage.git
   cd StatisticalArbitrage
   pip install -r requirements.txt
   python main.py
   