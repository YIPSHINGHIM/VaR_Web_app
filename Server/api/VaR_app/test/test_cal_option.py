import datetime as dt
import os
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Calculating_VaR_folder import Calculating_VaR
from Stock_data import Get_the_stock_data

period = 501

# * set up for single ticket
US_STOCK_LIST = ["TSLA"]
TSLA_100day_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)

# * set up for portfolio
US_STOCK_LIST = ["TSM","GOOGL","TSLA","MSFT","AAPL"]

portfolio_stock_data_100day = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)
print(portfolio_stock_data_100day.head())


cal_option_price = Calculating_VaR.cal_option_price

portfolio_obj = Calculating_VaR.cal_option_price('TSLA', 'call', 700, dt.datetime(2023, 6, 15), 0.015)

def test_cal_sigma():
    func_sigma = portfolio_obj.cal_sigma()["TSLA"]

    daily_returns = portfolio_obj.Calculating_daily_portfolio_Returns()

    daily_std = daily_returns.std()
    annual_std = daily_std * np.sqrt(252)

    sigma = (annual_std["TSLA"])
    assert abs(sigma - func_sigma) < 1e-10
    
    
def test_cal_d1_d2():
    
    S = TSLA_100day_data['TSLA'][-1]
    func_sigma = portfolio_obj.cal_sigma()["TSLA"]
    t = 10
    
    func_d1,func_d2 = portfolio_obj.cal_d1_d2(S, func_sigma, t)
    
    assert isinstance(func_d1, float)
    assert isinstance(func_d2, float)

def test_black_scholes():
    S = TSLA_100day_data['TSLA'][-1]
    func_sigma = portfolio_obj.cal_sigma()["TSLA"]
    t = 10
    
    price = portfolio_obj.black_scholes(S, func_sigma, t)
    assert isinstance(price, float)