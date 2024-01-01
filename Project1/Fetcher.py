'''
@project       : Temple University CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Brandon Zheng

@Date          : 10/7/2023

Download daily stock price from Yahoo

'''


import os
import pandas as pd
import numpy as np
import sqlite3

# pip install pandas-datareader
import pandas_datareader as pdr

import yfinance as yf

import option

# https://www.geeksforgeeks.org/python-stock-data-visualisation/

class Fetcher(object):

    def __init__(self, opt, db_connection):
        # opt is an option instance
        self.opt = opt
        self.db_connection = db_connection

    def get_daily_from_yahoo(self, ticker, start_date, end_date):
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        print("data", ticker)
        return df

    def download_data_to_csv(self, list_of_tickers):
        #
       for ticker in list_of_tickers:
            df = self.get_daily_from_yahoo(ticker, self.opt.start_date, self.opt.end_date)
            #add col
            df['Ticker'] = ticker
            #create <ticker>_daily.csv file
            output = os.path.join(self.opt.output_dir, f'{ticker}_daily.csv')
            df.to_csv(output)

            if df.shape[0] == 0:
                print(f"No data found for {ticker}")
    
        
    def csv_to_table(self, csv_file_name, fields_map, db_table):
        try:
            #data from csv to table
            df = pd.read_csv(csv_file_name)
            if df.shape[0] <= 0:
                return
            
            #change the column header
            df.columns = [fields_map[x] for x in df.columns]

            #move ticker columns
            new_df = df[['Ticker']].copy()
            for c in df.columns[:-1]:
                new_df[c] = df[c]

            ticker = os.path.basename(csv_file_name).replace('.csv','').replace("_daily", "")
            print(ticker)
            cursor = self.db_connection.cursor()
    
            #del old data from table
            del_sql = f"DELETE FROM {db_table} WHERE Ticker = ?"
            cursor.execute(del_sql, (ticker,))

            #df to tuples
            df_tuples = new_df.values.tolist()

            #insert new data into db
            insert_sql = f"INSERT INTO {db_table} (Ticker, AsOfDate, Open, High, Low, Close, Volume, Turnover, Dividend) VALUES ( ?, ?, ?, ?, ? ,?, ?, ?, ?)"
            print(insert_sql)
            cursor.executemany(insert_sql, df_tuples)

            #commit changes to db & close
            self.db_connection.commit()
            cursor.close()
        except Exception as e:
            print(f"An error has occured: {str(e)}")
        
    def save_daily_data_to_sqlite(self, daily_file_dir, list_of_tickers):
        # read daily_<ticker>.csv files
        db_table = 'EquityDailyPrice'

        fields_map = {'Date': 'AsOfDate', 'Dividends': 'Dividend', 'Stock Splits': 'StockSplits'}
        for f in ['Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']:
            fields_map[f] = f

        fields_map = {'Date': 'AsOfDate', 'Dividends': 'Dividend', 'Stock Splits': 'StockSplits'}
        for f in ['Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']:
            fields_map[f] = f

        for ticker in list_of_tickers:
            file_name = os.path.join(daily_file_dir, f"{ticker}_daily.csv")
            self.csv_to_table(file_name, fields_map, db_table)
            print("saved to DB: ", ticker)

    
def run():
    #
    parser = option.get_default_parser()
    parser.add_argument('--data_dir', dest = 'data_dir', default='./data', help='data dir')    
    
    args = parser.parse_args()
    opt = option.Option(args = args)

    opt.output_dir = os.path.join(opt.data_dir, "daily")
    opt.sqlite_db = os.path.join(opt.data_dir, "sqlitedb/Equity.db")
    
    if opt.tickers is not None:
        list_of_tickers = opt.tickers.split(',')
    else:
        fname = os.path.join(opt.data_dir, "S&P500.txt")
        list_of_tickers = list(pd.read_csv(fname, header=None).iloc[:, 0])
        print(f"Read tickers from {fname}")
        
    print(list_of_tickers)
    print(opt.start_date, opt.end_date)

    db_file = opt.sqlite_db
    db_connection = sqlite3.connect(db_file)
    
    fetcher = Fetcher(opt, db_connection)
    print(f"Download data to {opt.data_dir} directory")

    # Call the fetcher download and save_daily methods
    fetcher.download_data_to_csv(list_of_tickers)
    fetcher.save_daily_data_to_sqlite(opt.output_dir, list_of_tickers)
    
if __name__ == "__main__":
    #_test()
    run()

