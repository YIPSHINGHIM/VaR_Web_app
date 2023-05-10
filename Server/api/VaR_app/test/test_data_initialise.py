import datetime as dt
import os
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Calculating_VaR_folder import Calculating_VaR
from Stock_data import Get_the_stock_data

period = 100

# * set up for single ticket
US_STOCK_LIST = ["TSLA"]
TSLA_100day_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)
print(TSLA_100day_data["TSLA"][0])

# * set up for portfolio
US_STOCK_LIST = ["TSM","GOOGL","TSLA","MSFT","AAPL"]
portfolio_stock_data_100day = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)




#* test Calculating_daily_stock_Returns function for a single ticket
def test_Calculating_daily_stock_Returns_for_single_ticket():

    data_initialise_TSLA = Calculating_VaR.data_initialise(TSLA_100day_data)

    percentage_change = (TSLA_100day_data["TSLA"][1] - TSLA_100day_data["TSLA"][0])/TSLA_100day_data["TSLA"][0]

    TSLA_returns_df = data_initialise_TSLA.Calculating_daily_portfolio_Returns()


    func_ans = TSLA_returns_df["TSLA"][0]
    test_ans = percentage_change

    assert ("%.5f" % func_ans) == ("%.5f" % percentage_change)

# # #* test Calculating_daily_stock_Returns function for a portfolio (return)
def test_Calculating_daily_stock_Returns_for_portfolio():

    portfolio_weights = np.array([0.2,0.15,0.15,0.4,0.1])

    data_initialise_portfolio = Calculating_VaR.data_initialise(portfolio_stock_data_100day,portfolio_weights)

    portfolio_historical_return_df = data_initialise_portfolio.Calculating_daily_portfolio_Returns()

    # print(portfolio_historical_return_df.head())

    # prepare for the test 
    temp_df = portfolio_stock_data_100day.copy()
    temp_df = temp_df.pct_change()
    temp_df = temp_df.dropna()
    # print(temp_df.head())

    func_ans = (list(portfolio_historical_return_df.iloc[0]))
    test_ans = (list(temp_df.iloc[0]))

    assert func_ans == test_ans


# * test_adding the portfolio columns function  
def test_add_Portfolio_columns_to_df():

    portfolio_weights = np.array([0.2,0.15,0.15,0.4,0.1])

    data_initialise_portfolio = Calculating_VaR.data_initialise(portfolio_stock_data_100day,portfolio_weights)

    portfolio_historical_return_df = data_initialise_portfolio.Calculating_daily_portfolio_Returns()

    portfolio_historical_return_df_with_weights = data_initialise_portfolio.add_Portfolio_columns_to_df(portfolio_historical_return_df)

    # print(len(portfolio_historical_return_df_with_weights.columns))

    assert len(US_STOCK_LIST)+1 == len(portfolio_historical_return_df_with_weights.columns)

def test_quantile_to_VaR():
    data_init = Calculating_VaR.data_initialise(TSLA_100day_data)
    quantile = 0.95
    time = 10
    init_invest = 100000
    hVaR = quantile*np.sqrt(time)
    VaR = init_invest*hVaR *-1
    print(VaR)
    
    func_VaR = data_init.quantile_to_VaR(quantile,time,init_invest)
    print(func_VaR)
    
    assert abs(VaR - func_VaR) < 1e-10


def test_plot_graph():
    data_init = Calculating_VaR.data_initialise(TSLA_100day_data)
    prices = [10, 12, 13, 11, 10.5, 12, 13, 14, 15, 13.5]
    stock_name = 'TSLA'
    data_init.plot_graph(prices, stock_name)
    # Check that the file was saved
    import os
    from pathlib import Path
    assert os.path.exists(Path(__file__).parent.parent / 'images' / 'TSLA_MCS.png')

    





