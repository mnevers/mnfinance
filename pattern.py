import yfinance as yf
import time
import sys

def process_data(past,future):
    ticker = yf.Ticker("SPY")
    historical_data = ticker.history(start="2011-01-01", end="2024-10-04")    
    low = 0
    high = 0

    offset = 0
    low_days = 0
    high_days = 0    

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
        if val > high: #if at N time high
            if cnt+future < len(historical_data): #if not index greater that data set
                if historical_data['Close'].iloc[cnt+future] > val: #if F closing price is higher
                    high_days+=1
                elif historical_data['Close'].iloc[cnt+future] < val:#if f closing price lower
                    low_days+=1
            
    #print(f"{past} past days and {future} days in future")
    #print(f"High: {high_days}")
    #print(f"Low: {low_days}")
    return low_days,high_days


if __name__ == "__main__":    
    best = 0
    best_p = 0
    best_f = 0
    percent = 0    

    #60 is 3 months 20 business days in month about
    for p in range(59):
        for f in range(59):
            r = process_data(p+1,f+1)    
            print(f"{p+1},{f+1}")
            #time.sleep(.1)  # waiting so we don't overload API      
            percent = r[0] + r[1]
            percent = r[0]/percent

            if best < percent:
                best = percent
                best_p = p+1
                best_f = f+1
                print(f"Best Past: {best_p} Best Future: {best_f} Best Percent: {percent}")
    
    
    out = "Best Past days: " + str(best_p) + ", Best future days: " + str(best_f) + ". With a percentage of: " + str(percent) + "\n"
    print(out)

    text_file = open("Output.txt", "w")   
    
    text_file.write(out)
    text_file.close()


    