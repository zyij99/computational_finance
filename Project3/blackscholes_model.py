'''
@project       : Temple University CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : brandon zheng

@Date          : 12/2023

Black-Schole Model

'''

import datetime
from datetime import date
from scipy.stats import norm
from math import log, exp, sqrt

from stock import Stock
from financial_option import *

class BlackScholesModel(object):
    '''
    Implementation of the Black-Schole Model for pricing European options
    '''

    def __init__(self, pricing_date, risk_free_rate):
        self.pricing_date = pricing_date
        self.risk_free_rate = risk_free_rate

    def calc_parity_price(self, option, option_price):
        '''
        return the put price from Put-Call Parity if input option is a call
        else return the call price from Put-Call Parity if input option is a put
        '''
        result = None

        if option.option_type == FinancialOption.Type.CALL:
            result = option_price + option.strike * exp(-self.risk_free_rate * option.time_to_expiry) - option.underlying.spot_price
        elif option.option_type == FinancialOption.Type.PUT:
            result = option_price - option.strike * exp(-self.risk_free_rate * option.time_to_expiry) + option.underlying.spot_price
        
        return(result)

    def calc_model_price(self, option):
        '''
        Calculate the price of the option using Black-Scholes model
        '''
        px = None
        if option.option_style == FinancialOption.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        else:
            S0 = option.underlying.spot_price
            sigma = option.underlying.sigma
            T = option.time_to_expiry
            K = option.strike
            q = option.underlying.dividend_yield
            r = self.risk_free_rate

            d1 = (log(S0/K)+(r-q+pow(sigma, 2)/2)*T)/(sigma * sqrt(T))
            d2 = d1 - sigma * sqrt(T)

            if option.option_type == FinancialOption.Type.CALL:
                px = S0 * exp(-q * T) * norm.cdf(d1) - K * exp(-r * T) * norm.cdf(d2)
            elif option.option_type == FinancialOption.Type.PUT:
                px = K * exp(-r * T) * norm.cdf(-d2) - S0 * exp(-q * T) * norm.cdf(-d1)

        return(px)

    def calc_delta(self, option):
        if option.option_style == FinancialOption.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == FinancialOption.Style.EUROPEAN:
            S_0 = option.underlying.spot_price
            K = option.strike
            T = option.time_to_expiry
            r = self.risk_free_rate
            q = option.underlying.dividend_yield
            sigma = option.underlying.sigma
            
            d1 = (log(S_0/K)+(r-q+pow(sigma, 2)/2)*T)/(sigma * sqrt(T))
            if option.option_type == FinancialOption.Type.CALL:
                result = exp(-q * T) * norm.cdf(d1)
            elif option.option_type == FinancialOption.Type.PUT: 
                result = exp(-q * T) * (norm.cdf(d1) - 1)
        else:
            raise Exception("Unsupported option type")
        return result

    def calc_gamma(self, option):

        if option.option_style == FinancialOption.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == FinancialOption.Style.EUROPEAN:
            S_0 = option.underlying.spot_price
            K = option.strike
            T = option.time_to_expiry
            r = self.risk_free_rate
            q = option.underlying.dividend_yield
            sigma = option.underlying.sigma
            
            d1 = (log(S_0 / K) + (r - q + pow(sigma, 2) / 2) * T) / (sigma * sqrt(T))
            result = exp(-q * T) * norm.pdf(d1) / (S_0 * sigma * sqrt(T)) #Put & Call are the same
                                   
        else:
            raise Exception("Unsupported option type")
        return result

    def calc_theta(self, option):
        if option.option_style == FinancialOption.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == FinancialOption.Style.EUROPEAN:
            S_0 = option.underlying.spot_price
            K = option.strike
            T = option.time_to_expiry
            r = self.risk_free_rate
            q = option.underlying.dividend_yield
            sigma = option.underlying.sigma
            d1 = (np.log(S_0 / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * sqrt(T))
            d2 = d1 - sigma * sqrt(T)

            if option.option_type == FinancialOption.Type.CALL:
                result = (-S_0 * norm.pdf(d1) * sigma * exp(-q * T)) / (2 * sqrt(T)) + \
                    (q * S_0 * norm.cdf(d1) * exp(-q * T)) - (r * K * exp(-r * T) * norm.cdf(d2))
            elif option.option_type == FinancialOption.Type.PUT:
                result = (norm.pdf(d1) * exp(-q * T)) / (S_0 * sigma * sqrt(T)) - \
                    (q * S_0 * norm.cdf(-d1) * exp(-q * T)) + (r * K * exp(-r * T) * norm.cdf(-d2))
        else:
            raise Exception("Unsupported option type")
        return result

    def calc_vega(self, option):
        result = None

        if option.option_style == FinancialOption.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == FinancialOption.Style.EUROPEAN:
            S_0 = option.underlying.spot_price
            K = option.strike
            T = option.time_to_expiry
            r = self.risk_free_rate
            q = option.underlying.dividend_yield
            sigma = option.underlying.sigma
            d1 = (np.log(S_0 / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * sqrt(T))

            d1 = (log(S_0 / K) + (r - q + pow(sigma, 2) / 2) * T) / (sigma * sqrt(T))
            result = S_0 * sqrt(T) * norm.pdf(d1) * exp(-q * T) #Same put/call
        else:
            raise Exception("Unsupported option type")
        return result

    def calc_rho(self, option):
        result = None
        if option.option_style == FinancialOption.Style.AMERICAN:
            raise Exception("B\S price for American option not implemented yet")
        elif option.option_style == FinancialOption.Style.EUROPEAN:
            S_0 = option.underlying.spot_price
            K = option.strike
            T = option.time_to_expiry
            r = self.risk_free_rate
            q = option.underlying.dividend_yield
            sigma = option.underlying.sigma
            d1 = (np.log(S_0 / K) + (r - q + sigma ** 2 / 2) * T) / (sigma * sqrt(T))
            d2 = d1 - sigma * sqrt(T)

            if option.option_type == FinancialOption.Type.CALL:
                result = T * K * exp(-r * T) * norm.cdf(d2)
            elif option.option_type == FinancialOption.Type.PUT:
                result = -T * K * exp(-r * T) * norm.cdf(-d2)
        else:
            raise Exception("Unsupported option type")
        return result



def _test():
    import option
    import os
    import sqlite3

    opt = option.Option()
    opt.data_dir = "./data"
    opt.output_dir = os.path.join(opt.data_dir, "daily")
    opt.sqlite_db = os.path.join(opt.data_dir, "sqlitedb/Equity.db")
    db_file = opt.sqlite_db
    db_connection = sqlite3.connect(db_file)

    print(vars(opt))

    # Test BlackScholesModel class
    pricing_date = datetime.date(2023, 12, 8)

    # Create a simple European call option with specific values
    S0 = 42         #spot
    K = 40          #strike
    r = 0.1         #risk-free rate
    sigma = 0.2     #volatility
    T = 0.5         #time to expiry
    bs_model = BlackScholesModel(pricing_date, r)

    stock = Stock(opt, db_connection, 'AAPL', freq='quarterly', spot_price=S0, sigma=sigma)
    option_call = EuropeanCallOption(stock, time_to_expiry=T, strike=K)

    # Calculate option price using Black-Scholes model
    option_price = bs_model.calc_model_price(option_call)
    print('Option Call Price:', option_price)

    # Calculate delta, gamma, theta, vega, rho
    delta = bs_model.calc_delta(option_call)
    gamma = bs_model.calc_gamma(option_call)
    theta = bs_model.calc_theta(option_call)
    vega = bs_model.calc_vega(option_call)
    rho = bs_model.calc_rho(option_call)

    print('Delta Call:', delta)
    print('Gamma Call:', gamma)
    print('Theta Call:', theta)
    print('Vega Call:', vega)
    print('Rho Call:', rho)

    #put option
    option_put = EuropeanPutOption(stock, time_to_expiry=T, strike=K)
    # Calculate option put price using Black-Scholes model
    option_put_price = bs_model.calc_model_price(option_put)
    print('\nOption Put Price:', option_put_price)

    # Calculate put option Greeks
    delta_put = bs_model.calc_delta(option_put)
    gamma_put = bs_model.calc_gamma(option_put)
    theta_put = bs_model.calc_theta(option_put)
    vega_put = bs_model.calc_vega(option_put)
    rho_put = bs_model.calc_rho(option_put)

    print('Delta Put:', delta_put)
    print('Gamma Put:', gamma_put)
    print('Theta Put:', theta_put)
    print('Vega Put:', vega_put)
    print('Rho Put:', rho_put)


if __name__ == "__main__":
    _test()
