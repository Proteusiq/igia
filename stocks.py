from pathlib import Path
import pandas as pd


def get_stocks(url: str, file_name: str, last_trades: int = 1000) -> None:
    (
        pd.read_csv(url, usecols=["Date", "Adj Close"])
        .tail(last_trades)
        .rename(columns={"Date": "dato", "Adj Close": "worth"})
        .to_csv(file_name, index=False, compression="zip")
    )


if __name__ == "__main__":
    LAST_TRADES = 1000
    TICKER = "GOOG"
    STOCKS_URL = (
        f"https://query1.finance.yahoo.com/v7/finance/download/{TICKER}"
        "?period1=1104537600&period2=1681084800&interval=1d"
        "&events=history&includeAdjustedClose=true"
    )

    file_name = Path("./data/stocks.csv.zip")

    if not file_name.exists():
        print("Getting data ...")
        get_stocks(file_name = file_name, url=STOCKS_URL, last_trades=LAST_TRADES)
