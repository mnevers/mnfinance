import yfinance as yf
import time
import sys

def get_data(tic):
    ticker = yf.Ticker(tic)
    historical_data = ticker.history(start="2001-01-01", end="2024-10-04")
    print(len(historical_data))

    return historical_data

def process_data(past,historical_data):        
    low_days = 0
    high_days = 0    

    for cnt, val in enumerate(historical_data['Open']):       
        if cnt > past:#if we have enough hist data to process
            if val > historical_data['Close'].iloc[cnt-past]:   #if opened higher than prev closing day price         
                if val > historical_data['Close'].iloc[cnt]:
                    low_days+=1 #closed lower
                elif val < historical_data['Close'].iloc[cnt]:
                    high_days+=1 #closed higher

            
    return low_days,high_days

if __name__ == "__main__":    
    tic = "SPY"
    hist = get_data(tic)

    r = process_data(1,hist)
    t = r[0] + r [1]
    close_percent = r[0] / t

    out = tic + " closed lower percentage of time: " + str(close_percent) + "\n"
    print(out)


    