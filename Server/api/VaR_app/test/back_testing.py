import datetime as dt
import os
import sys
import time

import numpy as np
import pandas as pd
import yfinance as yf

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Calculating_VaR_folder import Calculating_VaR
from Stock_data import Get_the_stock_data

Time = 1
InitialInvestment = 10000
confidence_level= 5

# * set up for single ticket
US_STOCK_LIST = ["AAPL"]

# * set up for portfolio
US_STOCK_LIST = ["TSM","GOOGL","TSLA","MSFT","AAPL"]
portfolio_weights = np.array([0.2,0.15,0.15,0.4,0.1])


def download_data(tickers, start, end):
    data_have_nan = True
    data = None

    while data_have_nan:
        data = yf.download(tickers, start=start, end=end)['Close'].copy()
        
        if isinstance(data, pd.DataFrame):
            print("df is a DataFrame!")
        else:
            print("df is not a DataFrame.")
            data = data.to_frame()
        

        if data.isnull().any().any():
            print("The DataFrame contains NaN values")
            time.sleep(5)
        else:
            data_have_nan = False

    return data

AAPL_2018_2019 = download_data("AAPL", "2018-01-01", "2019-12-31")
AAPL_2020_2022 = download_data("AAPL", "2020-01-01", "2022-12-31")

Portfolio_2018_2019 = download_data("TSM GOOGL TSLA MSFT AAPL", "2018-01-01", "2019-12-31")
Portfolio_2020_2022 = download_data("TSM GOOGL TSLA MSFT AAPL", "2020-01-01", "2022-12-31")

cal_VaR_by_Historical_Simulation = Calculating_VaR.Historical_Simulation
cal_VaR_by_parametric_method = Calculating_VaR.parametric_method
cal_VaR_by_Monte_Carlo_Simulation_method = Calculating_VaR.Monte_Carlo_Simulation_method

def back_test_function(method,cal_VaR,data,portfolio_weights=np.array([1])):
    real_half_date = int(data.shape[0] - 1)/2
    half = int(int(data.shape[0] - 1)/2)

    
    # * testing set
    VaR_prediction_list = []

    for i in range(0,half):
        testing_set = data.iloc[i:(half+1)+i]
        VaR_prediction_list.append(cal_VaR(testing_set,method))
    
    VaR_prediction_list = (np.array(VaR_prediction_list))
    print(VaR_prediction_list.shape)

    # * real set
    if real_half_date %2 == 0 :
        real_set = data.iloc[half:]
    else:
        real_set = data.iloc[half:-1]
    # print(real_set)
    
    # calculating the returns 
    real_set_stock_object = method(real_set,portfolio_weights)
    real_set_df = real_set_stock_object.Calculating_daily_portfolio_Returns()
    real_set_df = real_set_stock_object.add_Portfolio_columns_to_df(real_set_df.copy())
    # print(real_set_df)
    
    real_set_var = real_set_df['Portfolio']*InitialInvestment*-1
    print(real_set_var.shape)
    # print(VaR_test_list)
    
    error_count = (real_set_var >= VaR_prediction_list).sum()
    # print(error_count)

    error_rate = (error_count/real_set_var.shape[0])
    # print(f'error rate = {round(error_rate*100,2)}%')
    print(error_rate)
    return error_rate 

# @ Testing section for Historical Simulation method

# *cal VaR function for Historical Simulation method
def cal_VaR_HS(testing_set,method,portfolio_weights=np.array([1])):
    stock_object = method(testing_set,portfolio_weights)
    VaR = (stock_object.Calculating_VaR_by_Historical_Simulation(confidence_level))
    hVaR = stock_object.quantile_to_VaR(VaR,Time,InitialInvestment)
    
    return(hVaR)


def test_back_testing_historical_simulation_AAPL_2018_2019():
    back_test_result = back_test_function(cal_VaR_by_Historical_Simulation,cal_VaR_HS,AAPL_2018_2019)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_back_testing_historical_simulation_Portfolio_2018_2019():
    back_test_result = back_test_function(cal_VaR_by_Historical_Simulation,cal_VaR_HS,Portfolio_2018_2019,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_back_testing_historical_simulation_AAPL_2020_2022():
    back_test_result = back_test_function(cal_VaR_by_Historical_Simulation,cal_VaR_HS,AAPL_2020_2022)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_back_testing_historical_simulation_Portfolio_2020_2022():
    back_test_result = back_test_function(cal_VaR_by_Historical_Simulation,cal_VaR_HS,Portfolio_2020_2022,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05
    
# @ Testing section for parametric method
# * method 1 
def cal_VaR_PM_1(testing_set,method,portfolio_weights=np.array([1])):
    stock_object = method(testing_set,portfolio_weights)
    VaR = (stock_object.Calculating_VaR_by_parametric_method(confidence_level,Time,InitialInvestment))
    
    return(VaR)

def test_back_testing_parametric_method_1_AAPL_2018_2019():
    back_test_result = back_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_1,AAPL_2018_2019)
    print(back_test_result)
    assert back_test_result <= 0.05
    
def test_back_testing_parametric_method_1_Portfolio_2018_2019():
    back_test_result = back_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_1,Portfolio_2018_2019,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_back_testing_parametric_method_1_AAPL_2020_2022():
    back_test_result = back_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_1,AAPL_2020_2022)
    print(back_test_result)
    assert back_test_result <= 0.05
    
def test_back_testing_parametric_method_1_Portfolio_2020_2022():
    back_test_result = back_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_1,Portfolio_2020_2022,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05
    
# * method 2 
def cal_VaR_PM_2(testing_set,method):
    stock_object = method(testing_set,portfolio_weights)
    VaR = (stock_object.Calculating_VaR_by_parametric_method_portfolio(confidence_level,Time,InitialInvestment))
    
    return(VaR)

def test_back_testing_parametric_method_2_AAPL_2018_2019():
    back_test_result = back_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_2,AAPL_2018_2019)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_back_testing_parametric_method_2_Portfolio_2018_2019():
    back_test_result = back_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_2,Portfolio_2018_2019,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_back_testing_parametric_method_2_AAPL_2020_2022():
    back_test_result = back_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_2,AAPL_2020_2022)
    print(back_test_result)
    assert back_test_result <= 0.05
    
def test_back_testing_parametric_method_2_Portfolio_2020_2022():
    back_test_result = back_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_2,Portfolio_2020_2022)
    print(back_test_result)
    assert back_test_result <= 0.05

# @ Testing section for Monte Carlo Simulation method

# # * method 1
def cal_VaR_MS_1(testing_set,method,portfolio_weights=np.array([1])):
    stock_object = method(testing_set,portfolio_weights)
    pdp = stock_object.predict_daily_price(501,1000)
    pdp_df_dict = stock_object.combine_the_predict_price(pdp)
    VaR , CVaR = (stock_object.using_HS_to_get_var(pdp_df_dict,Time,InitialInvestment,5))
    
    return VaR

def test_back_testing_monte_carlo_simulation_method_1_AAPL_2018_2019():
    back_test_result = back_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_1,AAPL_2018_2019)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_back_testing_monte_carlo_simulation_method_1_Portfolio_2018_2019():
    back_test_result = back_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_1,Portfolio_2018_2019,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_back_testing_monte_carlo_simulation_method_1_AAPL_2020_2022():
    back_test_result = back_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_1,AAPL_2020_2022)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_back_testing_monte_carlo_simulation_method_1_Portfolio_2020_2022():
    back_test_result = back_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_1,Portfolio_2020_2022,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05

# * method 2
def cal_VaR_MS_2(testing_set,method,portfolio_weights=np.array([1])):
    stock_object = method(testing_set,portfolio_weights)
    pdp = stock_object.predict_daily_price_cholesky_decomposition(501,1000)
    pdp_df_dict = stock_object.combine_the_predict_price(pdp)
    VaR , CVaR = (stock_object.using_HS_to_get_var(pdp_df_dict,Time,InitialInvestment,5))
    
    return VaR

def test_back_testing_monte_carlo_simulation_method_2_AAPL_2018_2019():
    back_test_result = back_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_2,AAPL_2018_2019)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_back_testing_monte_carlo_simulation_method_2_Portfolio_2018_2019():
    back_test_result = back_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_2,Portfolio_2018_2019,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_back_testing_monte_carlo_simulation_method_2_AAPL_2020_2022():
    back_test_result = back_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_2,AAPL_2020_2022)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_back_testing_monte_carlo_simulation_method_2_Portfolio_2020_2022():
    back_test_result = back_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_2,Portfolio_2020_2022,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05