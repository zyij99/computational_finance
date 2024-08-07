'''
@project       : CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : brandon zheng

@Date          : 10/28/2023

Script to run Discounted Cash Flow Model

'''

import os
import sqlite3
import option
import datetime

from DCF_model import DiscountedCashFlowModel
from stock import Stock

def get_eps_next_5Y(ticker):
    # return the EPS growth rate for the next 5Y by calling an API or reading from a database
    # However, for our own purpose, we read it from finviz.com and hard-coded the numbers here
    # 
    _data = {'AAPL': 0.0627, 
             'BABA': 0.1047, 
             'NVDA': 0.0765, 
             'JNJ': 0.0520, 
             'UBER': 0.2317, 
             'MSFT': 0.1620,
             'META': 0.3247,
             'PYPL': 0.1751,
             'ORCL': 0.1085,
             'JNPR': 0.1100,
             'AMD': 0.0980,
             'INTC': 0.0551,
             'MA': 0.2084
             }
    if ticker in _data.keys():
        return _data[ticker]
    else:
        print(f"No EPS growth rate found for {ticker}")
        return None

def run():
    #
    parser = option.get_default_parser()
    parser.add_argument('--data_dir', dest = 'data_dir', default='./data', help='data dir')    
    
    args = parser.parse_args()
    opt = option.Option(args = args)

    opt.output_dir = os.path.join(opt.data_dir, "daily")
    opt.sqlite_db = os.path.join(opt.data_dir, "sqlitedb/Equity.db")

    db_file = opt.sqlite_db
    db_connection = sqlite3.connect(db_file)
    
    if opt.tickers is not None:
        list_of_tickers = opt.tickers.split(',')
    
    else:
        list_of_tickers = ['AAPL']

    as_of_date = datetime.date(2023, 10, 1)

    for ticker in list_of_tickers:
        eps5y = get_eps_next_5Y(ticker)
        print(eps5y)

        stock = Stock(opt, db_connection, ticker)
        stock.load_financial_data()
        
        model = DiscountedCashFlowModel(stock, as_of_date)
        # long term eps growth rate is assumed to be at 4%
        model.set_FCC_growth_rate(eps5y, eps5y/2, 0.04)
        
        model_price = model.calc_fair_value()

        print(f"Fair value for {ticker} based on DCF is {model_price}")

if __name__ == "__main__":
    run()
    
