import yfinance as yf

def get_stock_info(ticker):

    try:

        stock = yf.Ticker(ticker)

        info = stock.info

        return {
            "name": info.get("longName"),
            "sector": info.get("sector"),
            "industry": info.get("industry"),
            "country": info.get("country"),
            "marketCap": info.get("marketCap")
        }

    except:

        return None
