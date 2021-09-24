import yfinance as yf

def load(ticker, start_date):
    df_stock_candidate = yf.download(ticker, start=start_date, progress=False)
    df_stock_candidate.index.name = "date"
    return df_stock_candidate
