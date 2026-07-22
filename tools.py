from langchain.tools import tool
import requests
from datetime import datetime

@tool("get_ytd_stats")
def get_ytd_stats(ticker: str) -> str:
    """
    Use this tool to get actual YTD performance for a stock ticker.
    Returns % change, high/low, last close, and volume.
    """
    try:
        now = int(datetime.now().timestamp())
        jan_1 = int(datetime(datetime.now().year, 1, 1).timestamp())
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?period1={jan_1}&period2={now}&interval=1d"
        r = requests.get(url)
        result = r.json()["chart"]["result"][0]
        quote = result["indicators"]["quote"][0]
        closes = quote["close"]
        highs = quote["high"]
        lows = quote["low"]
        volumes = quote["volume"]

        ytd_open = closes[0]
        last_close = closes[-1]
        pct = ((last_close - ytd_open) / ytd_open) * 100

        return (
            f"{ticker.upper()} is {pct:+.2f}% YTD.\n"
            f"• Jan Open: ${ytd_open:.2f}\n"
            f"• Last Close: ${last_close:.2f}\n"
            f"• High/Low: ${max(highs):.2f} / ${min(lows):.2f}\n"
            f"• Volume: {volumes[-1]:,}"
        )
    except Exception as e:
        return f"{ticker.upper()}: error fetching data ({e.__class__.__name__})"
