import yfinance as yf
import sys
from datetime import datetime, timedelta

def round_price(price):
    return round(price, 2) 

def get_mondays_and_fridays(year):
    current_year = datetime.now().year
    
    # If the parameter is 'none', use the previous year
    if year == "none":
        year = current_year
    else:
        year = int(year)

    if year > current_year:
        print("Year provided is in the future. Please provide a valid past or current year.")
        sys.exit(1)

    
    print("")
    print(f"Processing {ticker_symbol.upper()} historical data for: {year}")
    print("")

    # Define start and end date for the year
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    # If it's the current year, set the end date to today
    if year == current_year:
        end_date = datetime.now()

    # Find first Monday of the year
    day_of_week = start_date.weekday()  # Monday is 0, Sunday is 6
    first_monday = start_date + timedelta(days=(7 - day_of_week) % 7) if day_of_week != 0 else start_date

    # Initialize lists for mondays and fridays
    mondays_and_fridays = []

    # Generate all Mondays and Fridays starting from the first Monday
    current_monday = first_monday
    current_friday = first_monday + timedelta(days=4)

    while current_monday <= end_date or current_friday <= end_date:
        if current_monday <= end_date:
            mondays_and_fridays.append(current_monday.strftime("%Y-%m-%d"))
            current_monday += timedelta(days=7)

        if current_friday <= end_date:
            mondays_and_fridays.append(current_friday.strftime("%Y-%m-%d"))
            current_friday += timedelta(days=7)

    # Return list starting from first Monday
    return sorted([date for date in mondays_and_fridays if date >= first_monday.strftime("%Y-%m-%d")])

def get_price_difference(ticker_symbol, dates, year):
    # Define the start and end of the year for historical data
    ticker = yf.Ticker(ticker_symbol)
    up = 0
    down = 0
    lg_move = 0

    for i in range(0, len(dates), 2):
        if i + 1 >= len(dates):
            print(f"Skipping date pair at index {i}: incomplete pair.")
            continue

        friday_adjusted_end = (datetime.strptime(dates[i+1], "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        historical_data = ticker.history(start=dates[i], end=friday_adjusted_end) 
        first_date = historical_data['Open'].iloc[0]
        second_date = historical_data['Close'].iloc[-1]
        
        price_difference = second_date - first_date
        if price_difference > 0:
            up += 1            
        elif price_difference < 0:
            down += 1
            if price_difference < (first_date*.002):
                lg_move+=1

         # Output the results
        #print(f"Open price on {dates[i]}: {first_date}")
        #print(f"Close price on {dates[i+1]}: {second_date}")
        #print(f"Price difference: {price_difference:+.2f}")
        #print('---')  # Separator between results for readability

    total = up + down
    percent_up = (up / total) * 100
    percent_up = str(round_price(percent_up)) + "%"
    lg_mv_percent = (lg_move / total) * 100
    lg_mv_percent = str(round_price(lg_mv_percent)) + "%"

    print(f"Percentage of Time closed up: {percent_up}")
    print("")
    print(f"Percentage of Time closed up 0.2% or more: {lg_mv_percent}")
    print("")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python expected_move.py <ticker_symbol> [<year>]")
        sys.exit(1)

    ticker_symbol = sys.argv[1]
    year = sys.argv[2] if len(sys.argv) == 3 else "none" 

    dates = get_mondays_and_fridays(year) 
    get_price_difference(ticker_symbol,dates,year) 
