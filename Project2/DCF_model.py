'''
@project       : CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : brandon zheng

@Date          : 9/2023

Discounted Cash Flow Model with Financial Data from Yahoo Financial

https://github.com/JECSand/yahoofinancials


'''
import os
import pandas as pd
import numpy as np
import sqlite3
import datetime 
import math

import option
from stock import Stock

class DiscountedCashFlowModel(object):
    '''
    DCF Model:

    FCC is assumed to go have growth rate by 3 periods, each of which has different growth rate
           short_term_growth_rate for the next 5Y
           medium_term_growth_rate from 6Y to 10Y
           long_term_growth_rate from 11Y to 20thY
    '''

    def __init__(self, stock, as_of_date):
        self.stock = stock
        self.as_of_date = as_of_date

        self.short_term_growth_rate = None
        self.medium_term_growth_rate = None
        self.long_term_growth_rate = None


    def set_FCC_growth_rate(self, short_term_rate, medium_term_rate, long_term_rate):
        self.short_term_growth_rate = short_term_rate
        self.medium_term_growth_rate = medium_term_rate
        self.long_term_growth_rate = long_term_rate


    def calc_fair_value(self):
        '''
        calculate the fair_value using DCF model

        1. calculate a yearly discount factor using the WACC
        2. Get the Free Cash flow
        3. Sum the discounted value of the FCC for the first 5 years using the short term growth rate
        4. Add the discounted value of the FCC from year 6 to the 10th year using the medium term growth rate
        5. Add the discounted value of the FCC from year 10 to the 20th year using the long term growth rate
        6. Compute the PV as cash + short term investments - total debt + the above sum of discounted free cash flow
        7. Return the stock fair value as PV divided by num of shares outstanding

        '''
        
    
        try:
            eps5y = self.short_term_growth_rate 
            eps6to10y = self.medium_term_growth_rate
            eps10to20y = self.long_term_growth_rate 

            # Calculate discount factor using WACC
            wacc = self.stock.lookup_wacc_by_beta(self.stock.get_beta())
            discount_factor = 1 / (1 + wacc)

            # Get Free Cash Flow
            fcc = self.stock.get_free_cashflow()

            #init discount value vars
            sum_eps5y = 0
            sum_eps6to10y = 0
            sum_eps10to20y = 0

            # Calculate discounted values based on growth rates
            for years in range(1,6):  # year 1-5
                sum_eps5y += (fcc * math.pow((1 + eps5y), years) * math.pow(discount_factor, years))
                if years == 5:
                    fcc5 = fcc * math.pow((1 + eps5y), 5) #fcc at 5yrs

            for years in range(1, 6):  # year 6-10
                sum_eps6to10y += (fcc5 * math.pow((1 + eps6to10y), years) * math.pow(discount_factor, years+5))
                if years == 5: #this is year 10
                    fcc10 = fcc5 * math.pow(1+eps6to10y, 5) #fcc at 10yrs

            for years in range(1, 11):  # year 11-20
                sum_eps10to20y += (fcc10 * math.pow((1 + eps10to20y) , years) * math.pow(discount_factor, years+10))

            #sum of all the discount values
            sum_dv = sum_eps5y + sum_eps6to10y + sum_eps10to20y 

            #calculate present value
            cash_and_cash_equivalent = self.stock.get_cash_and_cash_equivalent()
            total_debt = self.stock.get_total_debt()
           
            present_val =  cash_and_cash_equivalent - total_debt + sum_dv

            num_shares_outstanding = self.stock.get_num_shares_outstanding()

            intrinsic_val = present_val / num_shares_outstanding
        
            return intrinsic_val
        
        except Exception as e:
            print(f"Error calculating the intrinsic value: {e}")
            return None
        

def _test1():
    '''
    Tie out with the result from the medium article. The final value for APPL should be 84.88
    '''

    # override the various financial data
    class StockForTesting(Stock):
        # Mark-up Stock object for testing and tie-out purpose
        def get_total_debt(self):
            result = 112723000000
            return(result)

        def get_free_cashflow(self):
            result = 71706000000
            return(result)

        def get_num_shares_outstanding(self):
            #from blog
            result = 17250000000
            return (result)

        def get_cash_and_cash_equivalent(self):
            #from blog
            result = 93025000000
            return(result)

        
        def get_beta(self):
            result = 1.31
            return(result)

    opt = None
    db_connection = None
    symbol = 'Testing AAPL'
    stock = StockForTesting(opt, db_connection, symbol)

    
    as_of_date = datetime.date(2020, 9, 28)
    model = DiscountedCashFlowModel(stock, as_of_date)

    print(f"Running test1 for {symbol} ")
    print("Shares ", stock.get_num_shares_outstanding())
    print("FCC ", stock.get_free_cashflow())
    beta = stock.get_beta()
    wacc = stock.lookup_wacc_by_beta(beta)
    print("Beta ", beta)
    print("WACC ", wacc)
    print("Total debt ", stock.get_total_debt())
    print("cash ", stock.get_cash_and_cash_equivalent())

    # look up EPS next 5Y from Finviz, 12.46% from the medium blog
    eps5y = 0.1246     
    model.set_FCC_growth_rate(eps5y, eps5y/2, 0.04)

    model_price = model.calc_fair_value()
    print(f"DCF price for {symbol} as of {as_of_date} is {model_price}")

def _test2():
    #
    eps5YData = {'AAPL': 0.074, 'BABA': 0.1058, 'TSLA': 0.0855, 'NVDA': 0.7870, 'JNJ': 0.0575 , 'MSFT' : .1620}
    
    symbol = 'AAPL'
    #symbol = 'BABA'
    #symbol = 'NVDA'
    #symbol = 'JNJ'
    #symbol = 'MSFT'
    
    # default option
    opt = option.Option()
    opt.data_dir = "./data"
    opt.output_dir = os.path.join(opt.data_dir, "daily")
    opt.sqlite_db = os.path.join(opt.data_dir, "sqlitedb/Equity.db")

    db_file = opt.sqlite_db
    db_connection = sqlite3.connect(db_file)
    
    as_of_date = datetime.date(2023, 10, 1)

    stock = Stock(opt, db_connection, symbol)
    stock.load_financial_data()
    
    model = DiscountedCashFlowModel(stock, as_of_date)

    print("Shares ", stock.get_num_shares_outstanding())
    print("FCC ", stock.get_free_cashflow())
    beta = stock.get_beta()
    wacc = stock.lookup_wacc_by_beta(beta)
    print("Beta ", beta)
    print("WACC ", wacc)
    print("Total debt ", stock.get_total_debt())
    print("cash ", stock.get_cash_and_cash_equivalent())

    # look up EPS next 5Y from Finviz, 12.46% from the medium blog
    eps5y = eps5YData[symbol]
    
    model.set_FCC_growth_rate(eps5y, eps5y/2, 0.04)

    model_price = model.calc_fair_value()
    print(f"DCF price for {symbol} as of {as_of_date} is {model_price}")
    

def _test():
    _test1()
    _test2()
    
if __name__ == "__main__":
    _test()
