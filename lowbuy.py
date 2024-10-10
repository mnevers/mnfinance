import yfinance as yf
import time
import sys

def get_data(tic):
    ticker = yf.Ticker(tic)
    historical_data = ticker.history(start="2011-01-01", end="2024-10-04")
    print(len(historical_data))

    return historical_data

def process_data(past,future,historical_data):        
    low_days = 0
    high_days = 0    
    low = 0
    high = 0

    offset = 0

    for cnt, val in enumerate(historical_data['Close']):       
        if cnt > past:#if we have enough hist data to process
            for n in range(past):# loop through past (20)$days                
                if n == 0: #init
                    low = historical_data['Close'].iloc[n+offset] 
                    high = historical_data['Close'].iloc[n+offset]
                else:
                    if historical_data['Close'].iloc[n+offset] < low:
                        low = historical_data['Close'].iloc[n+offset]
                    if historical_data['Close'].iloc[n+offset] > high:
                        high = historical_data['Close'].iloc[n+offset]
            offset+=1 #estabilish offset for n loop
            if val < low: #if at N time high or low
                if cnt+future < len(historical_data): #if not index greater that data set
                    temp = historical_data['Close'].iloc[cnt+future] - val
                    per = temp / val
                    if per > .1: #if F closing price is higher
                        high_days+=1
                    else:
                        low_days+=1
                        
                    
            
    return low_days,high_days

if __name__ == "__main__":    
    tic = "UPRO"
    hist = get_data(tic)

    r = process_data(1,10,hist)
    t = r[0] + r [1]
    close_percent = r[0] / t

    out = tic + " closed higher by .1 or more percentage of time: " + str(close_percent) + "\n"
    print(out)


    