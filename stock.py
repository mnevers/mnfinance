import yfinance as yf
import sys

def get_upcoming_earnings(ticker_symbol):
    # Create a Ticker object
    ticker = yf.Ticker(ticker_symbol)

    # Get earnings dates
    earnings_dates = ticker.earnings_dates

    print(earnings_dates)

def format_market_cap(market_cap):
    if market_cap >= 1e12:
        return f"{market_cap / 1e12:.3g}T"
    elif market_cap >= 1e9:
        return f"{market_cap / 1e9:.3g}B"
    elif market_cap >= 1e6:
        return f"{market_cap / 1e6:.3g}M"
    else:
        return f"{market_cap:.0f}"

def format_volume(volume):
    if volume >= 1e6:
        return f"{volume / 1e6:.3g}M"
    elif volume >= 1e3:
        return f"{volume / 1e3:.3g}K"
    else:
        return f"{volume:.0f}"

def round_price(price):
    return round(price, 2)

def get_stock_data(ticker):
    # Fetch the stock data
    stock = yf.Ticker(ticker)

    # Get common stock information
    data = {
        "Ticker": ticker.upper(),
        "Price": round_price(stock.history(period='1d')['Close'].iloc[-1]),                
        "Annual Dividend": round(stock.info.get('dividendRate', 0), 2) if isinstance(stock.info.get('dividendRate'), (int, float)) else 'N/A',
        "Dividend Yield": f"{round(stock.info.get('dividendYield', 0) * 100, 2)}%" if stock.info.get('dividendYield') is not None else 'N/A',
        "52 Week Low": round_price(stock.info.get('fiftyTwoWeekLow', 'N/A')),  # 52 week low        
        "52 Week High": round_price(stock.info.get('fiftyTwoWeekHigh', 'N/A')),  # 52 week high
        "Market Cap": format_market_cap(stock.info.get('marketCap', 'N/A')),
        "Volume": format_volume(stock.info.get('volume', 'N/A')),
        "Trailing PE": round(stock.info.get('trailingPE', 'N/A'), 2),
        "Forward PE": round(stock.info.get('forwardPE', 'N/A') , 2),
        "Revenue": format_market_cap(stock.info.get('totalRevenue', 'N/A')),
        "Net Income": format_market_cap(stock.info.get('netIncomeToCommon', 'N/A')),
        "Debt-to-Equity": round(stock.info.get('debtToEquity', 'N/A') / 100, 2) if isinstance(stock.info.get('debtToEquity'), (int, float)) else 'N/A',
        "Short Interest": f"{round(stock.info.get('shortPercentOfFloat', 0) * 100, 2)}%",    
    }
    
    return data

def print_stock_data(data):
    print("")
    for key, value in data.items():
        print(f"{key}: {value}")
    print("")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python stock.py <TICKER>")
        sys.exit(1)

    ticker = sys.argv[1]
    stock_data = get_stock_data(ticker)
    print_stock_data(stock_data)
