import yfinance as yf
import sys

def get_hist_data():
    ticker = yf.Ticker("SQQQ")
    historical_data = ticker.history(start="2011-01-01", end="2024-10-04")    
    low = 0
    high = 0

    for cnt, val in enumerate(historical_data['Close']):        
        if cnt == 0:
            low = historical_data['Close'].iloc[0]
            high = historical_data['Close'].iloc[0]
        


if __name__ == "__main__":
    get_hist_data()