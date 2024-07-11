'''
@project       : Temple University CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Brandon Zheng

@Date          : 9/15/2023

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

def get_daily_from_yahoo(ticker, start_date, end_date):
    try:
        stock = yf.Ticker(ticker)
        #call Yahoo history method to return a dataframe of daily price data
        df = stock.history(period="1d", start=start_date, end=end_date)
        return(df)
    except:
         print(f"error: failed to fetch data for {ticker}")
         return

def download_data_to_csv(opt, list_of_tickers):
    #
    '''
    iterate through the list of tickers, call the get_daily_from_yahoo between two dates
    specified from the option, save the dataframe to a csv file <ticker>_daily.csv in the output_dir
    remember to add a extra column with the ticker
    '''

    for ticker in list_of_tickers:
        df = get_daily_from_yahoo(ticker, opt.start_date, opt.end_date)
        if df is not None:
            #add col
            df['Ticker'] = ticker
            #create <ticker>_daily.csv file
            output = os.path.join(opt.output_dir, f'{ticker}_daily.csv')
            df.to_csv(output)
        else:
            print(f'error. skipping{ticker}')

def csv_to_table(csv_file_name, fields_map, db_connection, db_table):
    try:
        # insert data from a csv file to a table
        df = pd.read_csv(csv_file_name)
        if df.shape[0] <= 0:
            return
        # change the column header
        df.columns = [fields_map[x] for x in df.columns]

        # move ticker columns
        new_df = df[['Ticker']].copy()
        for c in df.columns[:-1]:
            new_df[c] = df[c]

        ticker = os.path.basename(csv_file_name).replace('.csv','').replace("_daily", "")
        print(ticker)
        cursor = db_connection.cursor()

        '''
        delete from the table any old data for the ticker
        hint: sql = f"delete from {db_table} .... ", then call execute
        turn the dataframe into tuples
        
        insert data by using a insert ... values statement under executemany method
        sql = f"insert into {db_table} (Ticker, AsOfDate, ...)  VALUES (?, ?, ...) "
        print(sql)
        '''
        
        #del old data
        del_sql = f"DELETE FROM {db_table} WHERE Ticker = ?"
        cursor.execute(del_sql, (ticker,))

        #df to tuples
        df_tuples = new_df.values.tolist()
        #insert into db
        insert_sql = f"INSERT INTO {db_table} (Ticker, AsOfDate, Open, High, Low, Close, Volume, Turnover, Dividend) VALUES ( ?, ?, ?, ?, ? ,?, ?, ?, ?)"
        print(insert_sql)
        cursor.executemany(insert_sql, df_tuples)

        #commit changes to db & close
        db_connection.commit()
        cursor.close()
    except Exception as e:
        print(f"An error has occured: {str(e)}")
    

def save_daily_data_to_sqlite(opt, daily_file_dir, list_of_tickers):
    # read all daily.csv files from a dir and load them into sqlite table
    db_file = os.path.join(opt.sqlite_db)
    db_conn = sqlite3.connect(db_file)
    db_table = 'EquityDailyPrice'
    
    fields_map = {'Date': 'AsOfDate', 'Dividends': 'Dividend', 'Stock Splits': 'StockSplits'}
    for f in ['Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']:
        fields_map[f] = f

    for ticker in list_of_tickers:
        file_name = os.path.join(daily_file_dir, f"{ticker}_daily.csv")
        print(file_name)
        csv_to_table(file_name, fields_map, db_conn, db_table)

    
def _test():
    ticker = 'MSFT'
    start_date = '2020-01-01'
    end_date = '2023-08-01'

    print (f"Testing getting data for {ticker}:")
    df = get_daily_from_yahoo(ticker, start_date, end_date)
    print(df)

def run():
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

    # download all daily price data into a output dir
    if 1:
        print(f"Download data to {opt.data_dir} directory")
        download_data_to_csv(opt, list_of_tickers)

    if 1:
        # read the csv file back and save the data into sqlite database
        save_daily_data_to_sqlite(opt, opt.output_dir, list_of_tickers)
    
if __name__ == "__main__":
    _test()
    run()
