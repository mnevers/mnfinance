import yfinance as yf
import sys
from termcolor import colored

def get_expected_move(ticker_symbol, expiration_date):
    # Get the options data for the specified ticker and expiration date
    ticker = yf.Ticker(ticker_symbol)

    if expiration_date != "none":
        options = ticker.option_chain(expiration_date)
    else:
        expiration_dates = ticker.options        
        expiration_date = expiration_dates[0]
        options = ticker.option_chain(expiration_date)

    # Get the current stock price
    current_price = ticker.history(period='1d')['Close'].iloc[-1]

    # Find ATM strike price (the nearest strike to the current price)
    strikes = options.calls['strike'].to_list()
    atm_strike = min(strikes, key=lambda x: abs(x - current_price))
    total_options_volume = options.calls['volume'].sum() + options.puts['volume'].sum()

    # Get ATM call and put prices
    atm_call_price = options.calls[options.calls['strike'] == atm_strike]['lastPrice'].values[0] if not options.puts[options.puts['strike'] == atm_strike].empty else 0
    atm_put_price = options.puts[options.puts['strike'] == atm_strike]['lastPrice'].values[0] if not options.puts[options.puts['strike'] == atm_strike].empty else atm_call_price
    
    if atm_call_price == 0:
        atm_call_price = atm_put_price

    # Calculate expected move
    expected_move = atm_call_price + atm_put_price
    expected_move = round(expected_move, 2)
    percentage_move = round((expected_move / current_price) * 100, 2) if current_price != 0 else 0
    percentage_move = str(percentage_move) + "%"

    # Output the results 
    print("")
    print(f"Ticker: {ticker_symbol.upper()}")
    print(f"Expiration Date: {expiration_date}")   
    print(f"Stock Price: {current_price:.2f}")  
    print(f"Total Options Volume: {total_options_volume}") 
    print(f"ATM Strike Price: {atm_strike}")
    print(f"ATM Call Price: {atm_call_price}")
    print(f"ATM Put Price: {atm_put_price}")    
    print(colored(f"Expected Move: {expected_move}", "yellow"))
    print(colored(f"Percentage Move: {percentage_move}", "yellow"))
    print("")

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python expected_move.py <ticker_symbol> [<expiration_date>]")
        sys.exit(1)

    ticker_symbol = sys.argv[1]
    expiration_date = sys.argv[2] if len(sys.argv) == 3 else "none"      

    get_expected_move(ticker_symbol, str(expiration_date))
