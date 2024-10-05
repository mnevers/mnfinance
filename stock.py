import yfinance as yf
import sys

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
    stock = yf.Ticker(ticker)
    data = {
        "Ticker": ticker.upper(),
        "Price": round_price(stock.history(period='1d')['Close'].iloc[-1]) if not stock.history(period='1d')['Close'].empty else 'N/A',  # Handle missing price
        "Annual Dividend": round(stock.info.get('dividendRate', 0), 2) if isinstance(stock.info.get('dividendRate'), (int, float)) else 'N/A',
        "Dividend Yield": f"{round(stock.info.get('dividendYield', 0) * 100, 2)}%" if isinstance(stock.info.get('dividendYield'), (int, float)) else 'N/A',
        "52 Week Low": round_price(stock.info.get('fiftyTwoWeekLow', 'N/A')) if isinstance(stock.info.get('fiftyTwoWeekLow'), (int, float)) else 'N/A', 
        "52 Week High": round_price(stock.info.get('fiftyTwoWeekHigh', 'N/A')) if isinstance(stock.info.get('fiftyTwoWeekHigh'), (int, float)) else 'N/A', 
        "Market Cap": format_market_cap(stock.info.get('marketCap', 'N/A')) if isinstance(stock.info.get('marketCap'), (int, float)) else 'N/A',
        "Volume": format_volume(stock.info.get('volume', 'N/A')) if isinstance(stock.info.get('volume'), (int, float)) else 'N/A',
        "Trailing PE": round(stock.info.get('trailingPE', 'N/A'), 2) if isinstance(stock.info.get('trailingPE'), (int, float)) else 'N/A',
        "Forward PE": round(stock.info.get('forwardPE', 'N/A'), 2) if isinstance(stock.info.get('forwardPE'), (int, float)) else 'N/A',
        "Revenue": format_market_cap(stock.info.get('totalRevenue', 'N/A')) if isinstance(stock.info.get('totalRevenue'), (int, float)) else 'N/A',
        "Net Income": format_market_cap(stock.info.get('netIncomeToCommon', 'N/A')) if isinstance(stock.info.get('netIncomeToCommon'), (int, float)) else 'N/A',
        "Debt-to-Equity": round(stock.info.get('debtToEquity', 'N/A') / 100, 2) if isinstance(stock.info.get('debtToEquity'), (int, float)) else 'N/A',
        "Short Interest": f"{round(stock.info.get('shortPercentOfFloat', 0) * 100, 2)}%" if isinstance(stock.info.get('shortPercentOfFloat'), (int, float)) else 'N/A',    
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
