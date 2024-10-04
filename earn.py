import yfinance as yf
import sys

def get_upcoming_earnings(ticker_symbol):
    # Create a Ticker object
    ticker = yf.Ticker(ticker_symbol)

    # Get earnings dates
    earnings_dates = ticker.earnings_dates

    print("")
    print(f"Ticker: {ticker_symbol.upper()}")
    print(earnings_dates)
    print("")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python earn.py <TICKER>")
        sys.exit(1)

    ticker = sys.argv[1]
    get_upcoming_earnings(ticker)