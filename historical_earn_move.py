import yfinance as yf
import sys
import pandas as pd
from datetime import datetime, timedelta
from termcolor import colored

def get_weekday_range(date_str):
    # Parse the input date string into a datetime object
    date_format = "%Y-%m-%d"
    date = datetime.strptime(date_str, date_format)
    
    # Find the previous valid weekday
    days_before = date - timedelta(days=1)
    while days_before.weekday() >= 5:  # Skip Saturday (5) and Sunday (6)
        days_before -= timedelta(days=1)
    
    # Find the next valid weekday
    days_after = date + timedelta(days=5)
    while days_after.weekday() >= 5:  # Skip Saturday (5) and Sunday (6)
        days_after += timedelta(days=1)

    # Return the valid weekdays
    return [days_before.date(), days_after.date()]


def round_price(price):
    return round(price, 2)

def get_earnings_history(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)

    earnings_dates = ticker.earnings_dates

    # Get current date as a timestamp
    current_date = datetime.now().strftime('%Y-%m-%d')

    # Filter out future earnings dates by converting the index to the same format
    earnings_dates = earnings_dates[earnings_dates.index < current_date]   
    print("")
    total = 0
    up = 0

    for d in earnings_dates.index.date:    
        date_range = get_weekday_range(str(d))
        historical_data = ticker.history(start=date_range[0], end=date_range[1])    

        #if after close else before close
        if earnings_dates.index.time[0].hour > 14:
            before = round_price(historical_data['Close'].iloc[1])
            after = round_price(historical_data['Close'].iloc[2])
        else:
            before = round_price(historical_data['Close'].iloc[0])
            after = round_price(historical_data['Close'].iloc[1])

        total+=1

        t = after - before
        move = str(round_price((abs(t) / before) * 100)) + "%"
        if after < before:
            move = "-"+move
        else:
            up+=1

        print(f"Earnings Date: {d}")
        print(f"Before: {before}")
        print(f"After: {after}")
        print(f"Percent Move: {move}")        
        print("")
        
    percent_up = round_price(up / total * 100)
    color = "yellow"

    if percent_up > 50:
        color = "green"
    elif percent_up < 50:
        color = "red" 

    percent_up = str(percent_up) + "%"
    
    print(colored(f"Percentage of times up: {percent_up}", color))   
    print("")
    

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python earn.py <TICKER>")
        sys.exit(1)

    ticker = sys.argv[1]
    get_earnings_history(ticker)
