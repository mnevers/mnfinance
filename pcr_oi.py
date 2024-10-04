import yfinance as yf
import sys
from termcolor import colored

def get_open_interest(ticker_symbol, expiration_date):
    # Get the options data for the specified ticker and expiration date
    ticker = yf.Ticker(ticker_symbol)

    if expiration_date != "none":
        options = ticker.option_chain(expiration_date)
    else:
        expiration_dates = ticker.options        
        expiration_date = expiration_dates[0]
        options = ticker.option_chain(expiration_date)

    # Calculate put and call open interest
    put_open_interest = options.puts['openInterest'].sum()
    call_open_interest = options.calls['openInterest'].sum()

    # Calculate the put/call ratio, handling the case where call_open_interest is zero
    pcr_open_interest = put_open_interest / call_open_interest if call_open_interest > 0 else None
    pcr_open_interest = round(pcr_open_interest, 2)

    color = "yellow"

    if pcr_open_interest > 1.1:
        color = "red"
    elif pcr_open_interest < .8:
        color = "green"

    # Output the results   
    print("")    
    print(f"Ticker: {ticker_symbol.upper()}")
    print(f"Expiration Date: {expiration_date}")  
    print(f"Put Open Interest: {put_open_interest}")
    print(f"Call Open Interest: {call_open_interest}")
    print(colored(f"Put/Call Ratio: {pcr_open_interest}", color))
    print("")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python pcr_oi.py <ticker_symbol> [<expiration_date>]")
        sys.exit(1)

    ticker_symbol = sys.argv[1]
    expiration_date = sys.argv[2] if len(sys.argv) == 3 else "none"
    
    get_open_interest(ticker_symbol, expiration_date)