from datetime import date
from django import forms

class CointegrationForm(forms.Form):
    current_year = date.today().year
    start_year = current_year - 10  # 10 years ago
    ticker_1 = forms.CharField(label='Ticker 1', max_length=10)
    ticker_2 = forms.CharField(label='Ticker 2', max_length=10)
    start_date = forms.DateField(
        label='Start Date',
        widget=forms.SelectDateWidget(years=range(start_year, current_year + 1))
    )
    end_date = forms.DateField(
        label='End Date',
        widget=forms.SelectDateWidget(years=range(start_year, current_year + 1))
    )