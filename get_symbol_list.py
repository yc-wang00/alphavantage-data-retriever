"""
Get the list of symbols from the API and save it to a csv file.
"""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
from config import conf_mgr
import pandas as pd

if __name__ == "__main__":
    CSV_URL = "https://www.alphavantage.co/query?function=LISTING_STATUS&apikey=demo"
    df = pd.read_csv(CSV_URL)
    df.to_csv(conf_mgr.list_symbol_csv_dir, index=False)
