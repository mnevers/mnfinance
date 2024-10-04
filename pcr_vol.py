import yfinance as yf
import sys
from termcolor import colored

def get_volume(ticker_symbol, expiration_date):
    # Get the options data for the specified ticker and expiration date
    ticker = yf.Ticker(ticker_symbol)

    if expiration_date != "none":
        options = ticker.option_chain(expiration_date)
    else:
        expiration_dates = ticker.options        
        expiration_date = expiration_dates[0]
        options = ticker.option_chain(expiration_date)

    # Calculate put and call volume
    put_volume = options.puts['volume'].sum()
    call_volume = options.calls['volume'].sum()

    # Calculate the put/call ratio, handling the case where call_volume is zero
    pcr_volume = put_volume / call_volume if call_volume > 0 else None
    pcr_volume = round(pcr_volume, 2)

    color = "yellow"

    if pcr_volume > 1.1:
        color = "red"
    elif pcr_volume < .8:
        color = "green"

    # Output the results 
    print("")
    print(f"Ticker: {ticker_symbol.upper()}")
    print(f"Expiration Date: {expiration_date}")     
    print(f"Put Volume: {put_volume}")
    print(f"Call Volume: {call_volume}")    
    print(colored(f"Put/Call Ratio: {pcr_volume}", color))
    print("")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python pcr_vol.py <ticker_symbol> [<expiration_date>]")
        sys.exit(1)

    ticker_symbol = sys.argv[1]
    expiration_date = sys.argv[2] if len(sys.argv) == 3 else "none"      

    get_volume(ticker_symbol, str(expiration_date))