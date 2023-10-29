"""
This module aims to implement the main function for retrieving data from alpha vantage
"""
# ───────────────────────────────────────────────────── imports ────────────────────────────────────────────────────── #
import csv
import json
import os
import pandas as pd
import itertools
import requests
import time

from tqdm import tqdm
from conf_manager import conf_mgr

# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #
#                                                     Data Retriever                                                   #
# ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────── #


def generate_month_list():
    """generate a list contain specific format of month. ex. 'year1month1', 'year1month2',..."""

    arr = []
    year_num = 2
    month_num = 12

    for i, j in itertools.product(range(1, year_num + 1), range(1, month_num + 1)):
        target_string = f"year{i}month{j}"
        arr.append(target_string)

    return arr


def get_stock_data_per_month(month, apikey, interval, stock_symbol):
    """retrieve stock data per month"""

    CSV_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY_EXTENDED&symbol={stock_symbol}&interval={interval}&slice={month}&apikey={apikey}"

    with requests.Session() as s:
        download = s.get(CSV_URL)
        decoded_content = download.content.decode("utf-8")
        cr = csv.reader(decoded_content.splitlines(), delimiter=",")
        my_list = list(cr)

    return my_list


def get_stock_data(stock_symbol, month_list, apikey):
    """retrieve a full 5 minutes data(2 years) from a stock, save to csv files"""

    for i, month in enumerate(month_list):
        data = get_stock_data_per_month(month=month, apikey=apikey, interval="5min", stock_symbol=stock_symbol)

        df = pd.DataFrame(data[1:], columns=data[0])

        if i == 0:
            df.to_csv(os.path.join(conf_mgr.data_stock_raw_dir, f"{stock_symbol}.csv"), index=False)
        else:
            df.to_csv(
                os.path.join(conf_mgr.data_stock_raw_dir, f"{stock_symbol}.csv"), index=False, mode="a", header=None
            )

        time.sleep(1)


def main():  # sourcery skip: raise-specific-error
    # load settings
    with open("setting.json", "r") as f:
        setting = json.load(f)

    apikey = setting["api_key"]

    try:
        df_symbol = pd.read_csv(conf_mgr.list_symbol_csv_dir)
    except FileNotFoundError:
        raise Exception("list_symbol_raw.csv not found, please run get_symbol_list.py first")

    today_date = "2022-11-18"
    filter_date = "2020-11-18"

    # select stock and ipodate is two years ago
    df_symbol_stock = df_symbol[(df_symbol["assetType"] == "Stock") & (df_symbol["ipoDate"] <= filter_date)]
    df_symbol_stock = df_symbol_stock.dropna(subset="name")

    # get symbols list
    symbols = df_symbol_stock.symbol.values
    # get month list
    month_list = generate_month_list()

    # iterate through all stocks to retrieve data
    for stock_symbol in tqdm(symbols):
        for attempt in range(10):
            try:
                get_stock_data(stock_symbol=stock_symbol, month_list=month_list, apikey=apikey)
                time.sleep(5)
            except Exception:
                continue
            else:
                break
        else:
            raise Exception("Connection break")


if __name__ == "__main__":
    main()
