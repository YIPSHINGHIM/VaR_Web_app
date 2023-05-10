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


cal_VaR_by_Historical_Simulation = Calculating_VaR.Historical_Simulation


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# * Testing section 

# * test_Calculating_VaR_by_Historical_Simulation_single_stock
def test_Calculating_VaR_by_Historical_Simulation_single_stock():
    confidence_level= 5

    TSLA_stock_object = cal_VaR_by_Historical_Simulation(TSLA_100day_data)

    TSLA_historical_return_df = (TSLA_stock_object.Calculating_daily_portfolio_Returns())

    TSLA_df_with_weights = TSLA_stock_object.add_Portfolio_columns_to_df(TSLA_historical_return_df)

    VaR = (TSLA_stock_object.Calculating_VaR_by_Historical_Simulation(confidence_level))

    assert VaR == np.percentile(TSLA_df_with_weights['Portfolio'],confidence_level)

# * test_Calculating_VaR_by_Historical_Simulation_portfolio
def test_Calculating_VaR_by_Historical_Simulation_portfolio():
    portfolio_weights = np.array([0.2,0.15,0.15,0.4,0.1])

    confidence_level= 5

    portfolio_stock_object = cal_VaR_by_Historical_Simulation(portfolio_stock_data_100day,portfolio_weights=portfolio_weights)

    portfolio_historical_return_df = (portfolio_stock_object.Calculating_daily_portfolio_Returns()).copy()


    portfolio_df_with_weights = portfolio_stock_object.add_Portfolio_columns_to_df(portfolio_historical_return_df)

    VaR = (portfolio_stock_object.Calculating_VaR_by_Historical_Simulation(confidence_level))

    # assert False
    assert VaR == np.percentile(portfolio_df_with_weights['Portfolio'],confidence_level)

# * test_Calculating_CVaR_by_Historical_Simulation_single_stock
def test_Calculating_CVaR_by_Historical_Simulation_single_stock():
    
    confidence_level= 5

    TSLA_stock_object = cal_VaR_by_Historical_Simulation(TSLA_100day_data)

    TSLA_historical_return_df = (TSLA_stock_object.Calculating_daily_portfolio_Returns())

    temp_df = TSLA_historical_return_df.copy()

    TSLA_df_with_weights = TSLA_stock_object.add_Portfolio_columns_to_df(temp_df)

    CVaR = (TSLA_stock_object.Calculating_CVaR_by_Historical_Simulation(confidence_level))

    belowVaR = TSLA_historical_return_df <= TSLA_stock_object.Calculating_VaR_by_Historical_Simulation(confidence_level)

    CVaR_in_test = TSLA_historical_return_df[belowVaR].mean()

    assert "%.5f" %CVaR == "%.5f" %CVaR_in_test[0]


def test_Calculating_CVaR_by_Historical_Simulation_portfolio():
    portfolio_weights = np.array([0.2,0.15,0.15,0.4,0.1])
    confidence_level= 5

    portfolio_stock_object = cal_VaR_by_Historical_Simulation(portfolio_stock_data_100day,portfolio_weights)

    portfolio_historical_return_df = (portfolio_stock_object.Calculating_daily_portfolio_Returns())


    temp_df = portfolio_historical_return_df.copy()

    portfolio_stock_df_with_weights = portfolio_stock_object.add_Portfolio_columns_to_df(temp_df)
    # print(portfolio_stock_df_with_weights.head())

    CVaR = (portfolio_stock_object.Calculating_CVaR_by_Historical_Simulation(confidence_level))

    belowVaR = portfolio_stock_df_with_weights['Portfolio'] <= portfolio_stock_object.Calculating_VaR_by_Historical_Simulation(confidence_level)

    CVaR_in_test = portfolio_stock_df_with_weights[belowVaR].mean()

    assert "%.5f" %CVaR == "%.5f" %CVaR_in_test['Portfolio']

# * test_quantile_to_VaR function
def test_quantile_to_VaR():

    TSLA_stock_object = cal_VaR_by_Historical_Simulation(TSLA_100day_data)
    
    quantile = 95
    Time = 1
    InitialInvestment = 10000

    func_ans = TSLA_stock_object.quantile_to_VaR(quantile,Time,InitialInvestment)

    temp_var = quantile*np.sqrt(Time)

    test_ans = InitialInvestment*temp_var *-1
    
    assert func_ans == test_ans


