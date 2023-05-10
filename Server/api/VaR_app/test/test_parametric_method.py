import datetime as dt
import os
import sys

import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Calculating_VaR_folder import Calculating_VaR
from Stock_data import Get_the_stock_data

period = 501
Time = 1
InitialInvestment = 10000

# * set up for single ticket
US_STOCK_LIST = ["TSLA"]
TSLA_100day_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)

# * set up for portfolio
US_STOCK_LIST = ["TSM","GOOGL","TSLA","MSFT","AAPL"]

portfolio_stock_data_100day = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)
print(portfolio_stock_data_100day.head())


cal_VaR_by_parametric_method = Calculating_VaR.parametric_method

# * Testing section 

def test_Calculating_VaR_by_parametric_methodn_1_single_stock():

    confidence_level= 5

    TSLA_stock_object = cal_VaR_by_parametric_method(TSLA_100day_data)

    TSLA_historical_return_df = (TSLA_stock_object.Calculating_daily_portfolio_Returns())

    TSLA_df_with_weights = TSLA_stock_object.add_Portfolio_columns_to_df(TSLA_historical_return_df)

    func_VaR = (TSLA_stock_object.Calculating_VaR_by_parametric_method(confidence_level,Time,InitialInvestment))

    TSLA_df_with_weights = TSLA_df_with_weights.copy()

    mu = np.mean(TSLA_df_with_weights['Portfolio'])
    # print(mu)
    
    # # Estimate the daily volatility => also = Standard Deviation
    vol = np.std(TSLA_df_with_weights['Portfolio'])

    quantile = norm.ppf(confidence_level/100 , mu,vol)

    hVaR = quantile*np.sqrt(Time)

    test_VaR = InitialInvestment*hVaR*-1

    assert func_VaR == test_VaR
    
def test_Calculating_VaR_by_parametric_methodn_1_portfolio():
    confidence_level= 5

    portfolio_object = cal_VaR_by_parametric_method(portfolio_stock_data_100day)

    TSLA_historical_return_df = (portfolio_object.Calculating_daily_portfolio_Returns())

    TSLA_df_with_weights = portfolio_object.add_Portfolio_columns_to_df(TSLA_historical_return_df)

    func_VaR = (portfolio_object.Calculating_VaR_by_parametric_method(confidence_level,Time,InitialInvestment))

    TSLA_df_with_weights = TSLA_df_with_weights.copy()

    mu = np.mean(TSLA_df_with_weights['Portfolio'])
    # print(mu)
    
    # # Estimate the daily volatility => also = Standard Deviation
    vol = np.std(TSLA_df_with_weights['Portfolio'])

    quantile = norm.ppf(confidence_level/100 , mu,vol)

    hVaR = quantile*np.sqrt(Time)

    test_VaR = InitialInvestment*hVaR*-1

    assert func_VaR == test_VaR
    

def test_Calculating_VaR_by_parametric_methodn_2_single_stock():
    portfolio_weights = np.array([1])
    confidence_level = 5

    TSLA_stock_object = cal_VaR_by_parametric_method(TSLA_100day_data,portfolio_weights)

    portfolio_returns_df = TSLA_stock_object.Calculating_daily_portfolio_Returns()

    func_VaR = TSLA_stock_object.Calculating_VaR_by_parametric_method_portfolio(confidence_level,Time,InitialInvestment)


    cov_matrix = portfolio_returns_df.copy().cov()

    amount_of_investing_for_each_stock = np.array([i*InitialInvestment for i in portfolio_weights])
        # print(amount_of_investing_for_each_stock)


    i = 0
    
    temp_list = []
    for row,cols in cov_matrix.items():
        # print(f'i = {i} row = {row} ')
        j = 0 
        for col in cols:
            temp_list.append(col*amount_of_investing_for_each_stock[i] * amount_of_investing_for_each_stock[j])
            j+=1
        i+=1


    # print(len(temp_list))
    # print(temp_list)
    temp_list = np.array(temp_list)

    sigma = np.sqrt(sum((temp_list)))

    # print(sigma)
    # scale is sigma(standard deviation)
    test_VaR = norm.ppf(confidence_level/100, scale=sigma) *np.sqrt(Time)*-1

    assert func_VaR == test_VaR    


def test_Calculating_VaR_by_parametric_methodn_2_portfolio():
    portfolio_weights = np.array([0.2,0.15,0.15,0.3,0.2])
    confidence_level = 5

    portfolio_stock_object = cal_VaR_by_parametric_method(portfolio_stock_data_100day,portfolio_weights)

    portfolio_returns_df = portfolio_stock_object.Calculating_daily_portfolio_Returns()

    func_VaR = portfolio_stock_object.Calculating_VaR_by_parametric_method_portfolio(confidence_level,Time,InitialInvestment)

    cov_matrix = portfolio_returns_df.copy().cov()

    amount_of_investing_for_each_stock = np.array([i*InitialInvestment for i in portfolio_weights])
        # print(amount_of_investing_for_each_stock)

    i = 0
    
    temp_list = []
    for row,cols in cov_matrix.items():
        # print(f'i = {i} row = {row} ')
        j = 0 
        for col in cols:
            temp_list.append(col*amount_of_investing_for_each_stock[i] * amount_of_investing_for_each_stock[j])
            j+=1
        i+=1


    # print(len(temp_list))
    # print(temp_list)
    temp_list = np.array(temp_list)

    sigma = np.sqrt(sum((temp_list)))

    # print(sigma)
    # scale is sigma(standard deviation)
    test_VaR = norm.ppf(confidence_level/100, scale=sigma) *np.sqrt(Time)*-1

    assert func_VaR == test_VaR