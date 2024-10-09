import yfinance as yf
import sys

def get_hist_data():
    ticker = yf.Ticker("SQQQ")
    historical_data = ticker.history(start="2011-01-01", end="2024-10-04")    
    low = 0
    high = 0
    days = 30
    offset = 0

    for cnt, val in enumerate(historical_data['Close']):
        if cnt > days:
            for n in range(days):
                if n == 0:
                    low = historical_data['Close'].iloc[n+offset]
                    high = historical_data['Close'].iloc[n+offset]
                else:
                    if historical_data['Close'].iloc[n+offset] < low:
                        low = historical_data['Close'].iloc[n+offset]
                    if historical_data['Close'].iloc[n+offset] > high:
                        high = historical_data['Close'].iloc[n+offset]
            offset+=1
           
    print(f"High: {high}")
    print(f"Low: {low}")


if __name__ == "__main__":
    get_hist_data()