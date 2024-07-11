'''
@project       : Temple University CIS 4360 Computational Methods in Finance
@Instructor    : Dr. Alex Pang

@Student Name  : Brandon Zheng

@Date          : 9/23/23

A Simple Mortgage Calculator
'''

import sys
import math
from bisection_method import bisection

class MortgageCalculator(object):

    def __init__(self, loan_amount, int_rate, term):
        self.loan_amount = loan_amount
        self.int_rate = int_rate
        self.term = term

    def _calc_next_month_balance(self, prev_balance, level_payment, int_rate):
        
        #Cpy & Paste from mortgage.py
        interest = prev_balance * int_rate/12 #annual interest rate -> monthly interest rate; 12 mon/year
        principal = level_payment - interest
        next_month_bal = prev_balance - principal
        return next_month_bal
    
    def _last_month_balance(self, level_payment):

        #cpy & paste, replace missing parameters from mortgage.py with self.<missing_param>
        prev_bal = self.loan_amount
 
        for _ in range(self.term * 12):
            prev_bal = self._calc_next_month_balance(prev_bal, level_payment, self.int_rate)
        
        return prev_bal
        
    def calc_level_payment(self):
        a = self.loan_amount * (1 + self.int_rate * self.term) / (12 * self.term)
        b = a/2
        def func(level_payment):
            return self._last_month_balance(level_payment)

        # call bisection with the func

        #dont need the iteration counter, therefore level_payment, _
        level_payment,_ = bisection(func, b, a, eps=.0000001)
        return level_payment

    def compute_level_payment_analytically(self):
        # use the analytical formula to compute the level payment
        #Formula: L = ((B_0 (1+r)^n) *n)/(((1+r)^n)-1)
        B_0 = self.loan_amount
        n = self.term * 12 #total num payments
        r = self.int_rate/12 #annual interest rate -> monthly interest rate; 12 mon/year
        
        level_payment = (B_0 * math.pow(1+r, n) * r) / (math.pow(1+r, n) - 1)
        return level_payment

    
def _test():
    #
    loan_amount = 240000
    int_rate = 0.05
    mortgage_term = 30

    mtgCalc = MortgageCalculator(loan_amount, int_rate, mortgage_term)
    print("this is using calc_level_payment() for test: ", mtgCalc.calc_level_payment())
    print("this is using compute_level_payment_analytically function for test: ", mtgCalc.compute_level_payment_analytically())
    #excel res: 1288.372

#TEST CASE 1
def _sampleCase1():
    loan_amount = 300000
    int_rate = 0.08
    mortgage_term = 35

    mtgCalc = MortgageCalculator(loan_amount, int_rate, mortgage_term)
    print("\nthis is using calc_level_payment() for sampleCase1: ", mtgCalc.calc_level_payment())
    print("this is using compute_level_payment_analytically function for sampleCase1: ", mtgCalc.compute_level_payment_analytically())
    #excel res: 2130.783

#TEST CASE 2
def _sampleCase2():
    loan_amount = 500000
    int_rate = 0.10
    mortgage_term = 50
    mtgCalc = MortgageCalculator(loan_amount, int_rate, mortgage_term)
    print("\nthis is using calc_level_payment() for sampleCase2: ", mtgCalc.calc_level_payment())
    print("this is using compute_level_payment_analytically function for sampleCase2: ", mtgCalc.compute_level_payment_analytically())
    #excel res: 4195.528

#TEST CASE 3
def _sampleCase3():
    loan_amount = 800000
    int_rate = 0.085
    mortgage_term = 40
    mtgCalc = MortgageCalculator(loan_amount, int_rate, mortgage_term)
    print("\nthis is using calc_level_payment() for sampleCase3: ", mtgCalc.calc_level_payment())
    print("this is using compute_level_payment_analytically function for sampleCase3: ", mtgCalc.compute_level_payment_analytically())
    #excel res: 5864.753


if __name__ == "__main__":
    _test()
    _sampleCase1()
    _sampleCase2()
    _sampleCase3()
