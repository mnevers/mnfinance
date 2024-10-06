import yfinance as yf
import sys
from datetime import datetime, timedelta

def round_price(price):
    return round(price, 2)

def get_quarters(year):
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

    # Initialize list for first and last weekdays of each month
    quarters = []
    year_str = str(year)

    quarters.append((year_str+"-01-01" , year_str+"-3-31"))
    quarters.append((year_str+"-04-01" , year_str+"-6-30"))
    quarters.append((year_str+"-07-01" , year_str+"-9-30"))
    quarters.append((year_str+"-10-01" , year_str+"-12-31"))

    return quarters

def get_price_difference(ticker_symbol, date_ranges, year):
    # Define the start and end of the year for historical data
    ticker = yf.Ticker(ticker_symbol)
    up = 0
    down = 0
    lg_move = 0

    for start_date, end_date in date_ranges:
        # Adjust the end date to the next day for `yfinance` to include the full data of the last weekday
        end_date_adjusted = (datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)).strftime("%Y-%m-%d")
        historical_data = ticker.history(start=start_date, end=end_date_adjusted)

        # Skip if no data is available
        if historical_data.empty:
            print(f"No data for the period {start_date} to {end_date}")
            continue

        first_date = historical_data['Open'].iloc[0]
        second_date = historical_data['Close'].iloc[-1]
        
        price_difference = second_date - first_date
        if price_difference > 0:
            up += 1
            if price_difference > (first_date * 0.02):
                lg_move += 1
        elif price_difference < 0:
            down += 1
        
        #print(f"Open price on {start_date}: {first_date}")
        #print(f"Close price on {end_date}: {second_date}")
        #print(f"Price difference: {price_difference:+.2f}")
        #print('---')  # Separator between results for readability

    total = up + down
    if total == 0:
        print("No valid data found for the given year.")
        return

    percent_up = (up / total) * 100
    percent_up = str(round_price(percent_up)) + "%"
    lg_mv_percent = (lg_move / total) * 100
    lg_mv_percent = str(round_price(lg_mv_percent)) + "%"

    print(f"Percentage of Time closed up: {percent_up}")
    print("")
    print(f"Percentage of Time closed up 2% or more: {lg_mv_percent}")
    print("")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python month_range_move.py <ticker_symbol> [<year>]")
        sys.exit(1)

    ticker_symbol = sys.argv[1]
    year = sys.argv[2] if len(sys.argv) == 3 else "none"

    date_ranges = get_quarters(year)
    get_price_difference(ticker_symbol, date_ranges, year)
