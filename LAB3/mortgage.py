'''
@project       : Temple University CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Brandon Zheng

@Date          : 9/22/2023

Basic Mortgage Calculation

'''

import sys
import math
from bisection_method import bisection

def calc_next_month_balance(prev_balance, level_payment, int_rate):
    # return next month balance 
    # TODO:

    interest = prev_balance * int_rate/12 #annual interest rate -> monthly interest rate; 12 mon/year
    principal = level_payment - interest
    next_month_bal = prev_balance - principal
    return next_month_bal

    # End TODO

def last_month_balance(loan_amount, int_rate, mortgage_term, level_payment):
    # calculate the last month remaining balance
    # mortgage_term is the number of years for the mortgage
    # int_rate is the annual interest rate in fraction

    prev_bal = loan_amount

    # TODO:
    for _ in range(mortgage_term * 12):
        prev_bal = calc_next_month_balance(prev_bal, level_payment, int_rate)
        
    # End TODO
    return(prev_bal)


def calc_level_payment(loan_amount, int_rate, mortgage_term):
    # calculate the level payment by defining a function that return the last month balance
    # then use the bisection method to require the last month balance to be zero
    a = loan_amount * (1+int_rate * mortgage_term)/(12*mortgage_term)
    b = a/2
    # TODO:

    def func(level_payment):
        return last_month_balance(loan_amount, int_rate, mortgage_term, level_payment)

    # call bisection with the func

    #dont need the iteration counter, therefore level_payment, _
    level_payment,_ = bisection(func, b, a, eps=.0000001)
    return level_payment

    # End TODO
    
def test():
    loan_amount = 240000
    int_rate = 0.05
    term = 30
    level_payment = loan_amount * (1+int_rate * term)/(12*term) / 2
    #Added "this is ... " so it's clearer what's being displayed when I run this.
    print("this is the level payment test:", level_payment)
    print("this is the last month bal test:" , last_month_balance(loan_amount, int_rate, term, level_payment))
    #excel res: 833.333
          
def run():
    #
    loan_amount = 240000
    int_rate = 0.05
    mortgage_term = 30
    #Added "this is ... " so it's clearer what's being displayed when I run this.
    print("this is the level payment: ", calc_level_payment(loan_amount, int_rate, mortgage_term))
    #excel res: 1288.372

#TEST CASE 1
def sampleCase1():
    loan_amount = 300000
    int_rate = 0.08
    mortgage_term = 35
    print("This is sample case 1's level payment: ", calc_level_payment(loan_amount, int_rate, mortgage_term))
    #excel res: 2130.783

#TEST CASE 2
def sampleCase2():
    loan_amount = 500000
    int_rate = 0.10
    mortgage_term = 50
    print("This is sample case 2's level payment: ", calc_level_payment(loan_amount, int_rate, mortgage_term))
    #excel res: 4195.528

#TEST CASE 3
def sampleCase3():
    loan_amount = 800000
    int_rate = 0.085
    mortgage_term = 40
    print("This is sample case 3's level payment: ", calc_level_payment(loan_amount, int_rate, mortgage_term))   
    #excel res: 5864.753


if __name__ == "__main__":
    test()
    run()
    sampleCase1()
    sampleCase2()
    sampleCase3()