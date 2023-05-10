import datetime as dt
import os
import sys

import numpy as np
import pandas as pd
import yfinance as yf
from scipy.stats import norm

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Calculating_VaR_folder.Calculating_VaR import \
    Monte_Carlo_Simulation_method
from Stock_data import Get_the_stock_data

period = 501
Time = 1
InitialInvestment = 10000

# * set up for single ticket
US_STOCK_LIST = ["TSLA"]
TSLA_501day_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)

# * set up for portfolio
US_STOCK_LIST = ["TSM","GOOGL","TSLA","MSFT","AAPL"]

portfolio_stock_data_501ay = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)

TSLA_stock_object = Monte_Carlo_Simulation_method(TSLA_501day_data)

portfolio_object = Monte_Carlo_Simulation_method(portfolio_stock_data_501ay)

# * Testing section 

def test_logarithmic_returns_single_stock():

    TSLA_historical_return_df = (TSLA_stock_object.Calculating_daily_portfolio_Returns())

    func_logarithmic_returns = TSLA_stock_object.logarithmic_returns()
    
    daily_return = TSLA_historical_return_df+1
    test_logarithmic_returns = daily_return.apply(np.log)
    
    result = list(func_logarithmic_returns.head()) == list(test_logarithmic_returns.head())
    
    assert result
    
def test_logarithmic_returns_portfolio():

    portfolio_historical_return_df = (portfolio_object.Calculating_daily_portfolio_Returns())

    func_logarithmic_returns = portfolio_object.logarithmic_returns()
    
    daily_return = portfolio_historical_return_df+1
    test_logarithmic_returns = daily_return.apply(np.log)
    
    result = list(func_logarithmic_returns.head()) == list(test_logarithmic_returns.head())
    
    assert result
  
def test_compute_drift_single_stock():
    log_returns = TSLA_stock_object.logarithmic_returns()
    
    u = log_returns.mean()
    var = log_returns.var()
    test_drift = u - (0.5*var)
    test_drift = list(test_drift)
    
    func_drift = list(TSLA_stock_object.compute_drift())
    
    assert func_drift == test_drift
    
def test_compute_drift_portfolio():
    log_returns = portfolio_object.logarithmic_returns()
    
    u = log_returns.mean()
    var = log_returns.var()
    test_drift = u - (0.5*var)
    test_drift = list(test_drift)
    
    func_drift = list(portfolio_object.compute_drift())
    
    assert func_drift == test_drift
  
def test_predict_daily_price_single_stock():
    period = 5
    iterations = 10

    func_predict_daily_price = TSLA_stock_object.predict_daily_price(period,iterations)
    
    func_keys = func_predict_daily_price.keys()
    func_values = list(func_predict_daily_price.values())
    
    
    closing_price_df = TSLA_stock_object.Stock_historical_data_df
    
    log_returns = TSLA_stock_object.logarithmic_returns()
    drift = TSLA_stock_object.compute_drift()
    
    stdev = log_returns.std()
    temp_stock_list = list((log_returns.columns))
    
    all_simulation = {}
    for stock in temp_stock_list:
        
        pdr = np.exp(drift[stock] + stdev[stock] * norm.ppf(np.random.rand(period,iterations)))
        # print(pdr)
        price_list = np.zeros_like(pdr)
        price_list[0] = closing_price_df[stock].iloc[-1]
        
        for t in range(1,period):
            price_list[t] = price_list[t-1]*pdr[t]
            
        # print(price_list)
        temp_df = pd.DataFrame(price_list)        
        all_simulation[stock] = temp_df
            
    
    test_keys = all_simulation.keys()
    test_values = list(all_simulation.values())
    
    assert (func_keys == test_keys and func_values[0].shape == test_values[0].shape)
        
def test_predict_daily_price_portfolio():
    period = 5
    iterations = 10

    func_predict_daily_price = portfolio_object.predict_daily_price(period,iterations)
    
    func_keys = func_predict_daily_price.keys()
    func_values = list(func_predict_daily_price.values())
    
    
    closing_price_df = portfolio_object.Stock_historical_data_df
    
    log_returns = portfolio_object.logarithmic_returns()
    drift = portfolio_object.compute_drift()
    
    stdev = log_returns.std()
    temp_stock_list = list((log_returns.columns))
    
    all_simulation = {}
    for stock in temp_stock_list:
        
        pdr = np.exp(drift[stock] + stdev[stock] * norm.ppf(np.random.rand(period,iterations)))
        # print(pdr)
        price_list = np.zeros_like(pdr)
        price_list[0] = closing_price_df[stock].iloc[-1]
        
        for t in range(1,period):
            price_list[t] = price_list[t-1]*pdr[t]
            
        # print(price_list)
        temp_df = pd.DataFrame(price_list)        
        all_simulation[stock] = temp_df
            
    test_keys = all_simulation.keys()
    test_values = list(all_simulation.values())
    
    print(func_keys == test_keys)
    
    print(func_values[0].shape)
    print(test_values[0].shape)
    
    
    assert (func_keys == test_keys and func_values[0].shape == test_values[0].shape)
    
def test_predict_daily_price_cholesky_decomposition_single_stock():
    
    period = 5
    iterations = 10

    func_predict_daily_price = TSLA_stock_object.predict_daily_price_cholesky_decomposition(period,iterations)
    
    func_keys = func_predict_daily_price.keys()
    func_values = list(func_predict_daily_price.values())
    
    
    closing_price_df = TSLA_stock_object.Stock_historical_data_df
    
    log_returns = TSLA_stock_object.logarithmic_returns()
    drift = TSLA_stock_object.compute_drift()
    temp_stock_list = list((log_returns.columns))
    numstocks = len(temp_stock_list)
    
    covari = log_returns.cov()
    chol = np.linalg.cholesky(covari)

    uncorr_x = norm.ppf(np.random.rand(numstocks,iterations*period))
    corr_x = np.dot(chol, uncorr_x)
    
    corr_2 = np.zeros_like(corr_x)
    for i in range(numstocks):
        corr_2[i] = np.exp(drift[i] + corr_x[i]) 
        
    all_simulation = {}
    
    stock_index = 0
    for stock in temp_stock_list:
        
        ret_reshape = corr_2[stock_index]
        ret_reshape = ret_reshape.reshape(period,iterations)

        price_list = np.zeros_like(ret_reshape)
        price_list[0] = closing_price_df[stock].iloc[-1]
        
        for t in range(1,period):
            price_list[t] = price_list[t-1]*ret_reshape[t]
            
        # print(price_list)
        temp_df = pd.DataFrame(price_list)        
        all_simulation[stock] = temp_df
        
        stock_index +=1

    test_keys = all_simulation.keys()
    test_values = list(all_simulation.values())
    
    assert (func_keys == test_keys and func_values[0].shape == test_values[0].shape)
    
def test_predict_daily_price_cholesky_decomposition_single_stock():
    
    period = 5
    iterations = 10

    func_predict_daily_price = portfolio_object.predict_daily_price_cholesky_decomposition(period,iterations)
    
    func_keys = func_predict_daily_price.keys()
    func_values = list(func_predict_daily_price.values())
    
    
    closing_price_df = portfolio_object.Stock_historical_data_df
    
    log_returns = portfolio_object.logarithmic_returns()
    drift = portfolio_object.compute_drift()
    temp_stock_list = list((log_returns.columns))
    numstocks = len(temp_stock_list)
    
    covari = log_returns.cov()
    chol = np.linalg.cholesky(covari)

    uncorr_x = norm.ppf(np.random.rand(numstocks,iterations*period))
    corr_x = np.dot(chol, uncorr_x)
    
    corr_2 = np.zeros_like(corr_x)
    for i in range(numstocks):
        corr_2[i] = np.exp(drift[i] + corr_x[i]) 
        
    all_simulation = {}
    
    stock_index = 0
    for stock in temp_stock_list:
        
        ret_reshape = corr_2[stock_index]
        ret_reshape = ret_reshape.reshape(period,iterations)

        price_list = np.zeros_like(ret_reshape)
        price_list[0] = closing_price_df[stock].iloc[-1]
        
        for t in range(1,period):
            price_list[t] = price_list[t-1]*ret_reshape[t]
            
        # print(price_list)
        temp_df = pd.DataFrame(price_list)        
        all_simulation[stock] = temp_df
        
        stock_index +=1

    test_keys = all_simulation.keys()
    test_values = list(all_simulation.values())
    
    assert (func_keys == test_keys and func_values[0].shape == test_values[0].shape)