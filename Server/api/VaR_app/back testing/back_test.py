import datetime as dt
import os
import sys

import numpy as np
import pandas as pd
import yfinance as yf

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Calculating_VaR import Calculating_VaR
from Stock_data import Get_the_stock_data

back_test_period = 101
period = 201

# * set up for single ticket
US_STOCK_LIST = ["TSLA"]

TSLA_100day_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)

# * set up for portfolio
US_STOCK_LIST = ["TSM","GOOGL","TSLA","MSFT","AAPL"]

portfolio_stock_data_100day = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)


cal_VaR_by_Historical_Simulation = Calculating_VaR.Historical_Simulation

def back_testing_Calculating_VaR_by_Historical_Simulation_single_stock():
    
    confidence_level= 5
    InitialInvestment = 10000

    # * train set
    train_set = TSLA_100day_data.iloc[:101]
    # print(train_set)    

    # TSLA_stock_object = cal_VaR_by_Historical_Simulation(train_set)

    # TSLA_historical_return_df = (TSLA_stock_object.Calculating_daily_portfolio_Returns())

    # VaR = (TSLA_stock_object.Calculating_VaR_by_Historical_Simulation(TSLA_historical_return_df['TSLA'],confidence_level))

    # print(VaR)

    # basic case :
    def cal_VaR(train_set):
        TSLA_stock_object = cal_VaR_by_Historical_Simulation(train_set)

        TSLA_historical_return_df = (TSLA_stock_object.Calculating_daily_portfolio_Returns())

        VaR = (TSLA_stock_object.Calculating_VaR_by_Historical_Simulation(TSLA_historical_return_df['TSLA'],confidence_level))

        return(VaR)

    # print(cal_VaR(train_set))

    # train_set = TSLA_100day_data.iloc[5:106]
    # print(cal_VaR(train_set))

    VaR_prediction_list = []

    for i in range(0,100):
        train_set = TSLA_100day_data.iloc[i:101+i]

        VaR_prediction_list.append(cal_VaR(train_set))
    
    
    VaR_prediction_list = (np.array(VaR_prediction_list))
    VaR_prediction_list = VaR_prediction_list*-1
    VaR_prediction_list = (VaR_prediction_list*InitialInvestment)

    # print(VaR_prediction_list)
    # print(VaR_prediction_list.shape)



    # * test set
    test_set = TSLA_100day_data.iloc[100:]
    # print(test_set.shape)
    # print(test_set)

    # calculating the returns 
    test_set_return_df = test_set.pct_change()
    test_set_return_df = test_set_return_df.dropna()
    test_set_return_df = test_set_return_df*-1


    # print(test_set_return_df)
    # print(test_set_return_df.shape)
    # print(test_set_return_df*InitialInvestment)
    VaR_test_list = (test_set_return_df*InitialInvestment)["TSLA"]

    # print(VaR_test_list)

    # print(VaR_test_list[0])
    error_list = []

    for i in range(0,100):
        if VaR_test_list[i] >= VaR_prediction_list[i]:
            error_list.append(1)
        else:
            error_list.append(0)

    # print(error_list)

    error_rate = (sum(error_list)/len(error_list))
    print(f'error rate = {round(error_rate*100,2)}%')


    return error_rate
    
print('back testing Calculating VaR by Historical Simulation single stock')
back_testing_Calculating_VaR_by_Historical_Simulation_single_stock()
print('--------------------------------------')

    
def back_testing_Calculating_VaR_by_Historical_Simulation_portfolio():
    
    confidence_level= 5
    InitialInvestment = 10000
    portfolio_weights = np.array([0.2,0.15,0.15,0.3,0.2])
    US_STOCK_LIST = ["TSM","GOOGL","TSLA","MSFT","AAPL"]

    # * predict set
    train_set = portfolio_stock_data_100day.iloc[:101]
    # print(train_set)    

    # basic case :
    def cal_VaR(train_set):
        portfolio_stock_object = cal_VaR_by_Historical_Simulation(train_set,portfolio_weights)

        portfolio_historical_return_df = (portfolio_stock_object.Calculating_daily_portfolio_Returns())

        portfolio_df_with_weights = portfolio_stock_object.add_Portfolio_columns_to_df(portfolio_historical_return_df)

        VaR = (portfolio_stock_object.Calculating_VaR_by_Historical_Simulation(portfolio_df_with_weights['Portfolio'],confidence_level))

        # print(portfolio_df_with_weights)

        return(VaR)

    VaR_prediction_list = []

    for i in range(0,100):
        train_set = portfolio_stock_data_100day.iloc[i:101+i]

        VaR_prediction_list.append(cal_VaR(train_set))
    
    
    VaR_prediction_list = (np.array(VaR_prediction_list))
    VaR_prediction_list = VaR_prediction_list*-1
    VaR_prediction_list = (VaR_prediction_list*InitialInvestment)

    # print(VaR_prediction_list)
    # print(VaR_prediction_list.shape)

    # * test set
    test_set = portfolio_stock_data_100day.iloc[100:]
    # print(test_set.shape)
    # print(test_set)

    test_object =cal_VaR_by_Historical_Simulation(test_set,portfolio_weights)

    # calculating the returns 
    test_set_return_df = test_set.pct_change()
    test_set_return_df = test_set_return_df.dropna()
    test_set_return_df = test_set_return_df*-1

    test_set_return_df_df_with_weights = test_object.add_Portfolio_columns_to_df(test_set_return_df)
    # print(test_set_return_df_df_with_weights)

    
    VaR_test_list = (test_set_return_df_df_with_weights["Portfolio"]*InitialInvestment)

    error_list = []

    for i in range(0,100):
        if VaR_test_list[i] >= VaR_prediction_list[i]:
            error_list.append(1)
        else:
            error_list.append(0)

    # print(error_list)

    error_rate = (sum(error_list)/len(error_list))
    print(f'error rate = {round(error_rate*100,5)}%')


    return error_rate

print('back testing Calculating VaR by Historical Simulation portfolio')
back_testing_Calculating_VaR_by_Historical_Simulation_portfolio()
