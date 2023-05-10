import datetime as dt
import os
import sys

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
AAPL_201day_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,201)


AAPL_1001day_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,1001)

# * set up for portfolio
US_STOCK_LIST = ["TSM","GOOGL","TSLA","MSFT","AAPL"]
portfolio_weights = np.array([0.2,0.15,0.15,0.4,0.1])

portfolio_stock_data_201day = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,201)

portfolio_stock_data_1001day = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,1001)

cal_VaR_by_Historical_Simulation = Calculating_VaR.Historical_Simulation
cal_VaR_by_parametric_method = Calculating_VaR.parametric_method
cal_VaR_by_Monte_Carlo_Simulation_method = Calculating_VaR.Monte_Carlo_Simulation_method


# TODO can use switch to do make the cal var function

def stress_test_function(method,cal_VaR,data,portfolio_weights=np.array([1])):
    half = int(int(data.shape[0] - 1)/2)
    # * testing set
    VaR_prediction_list = []

    for i in range(0,half):
        testing_set = data.iloc[i:(half+1)+i]
        VaR_prediction_list.append(cal_VaR(testing_set,method))
    
    VaR_prediction_list = (np.array(VaR_prediction_list))
    # print(VaR_prediction_list)

    # * real set
    real_set = data.iloc[half:]
    # print(real_set)
    
    # calculating the returns 
    real_set_stock_object = method(real_set,portfolio_weights)
    real_set_df = real_set_stock_object.Calculating_daily_portfolio_Returns()
    real_set_df = real_set_stock_object.add_Portfolio_columns_to_df(real_set_df.copy())
    # print(real_set_df)
    
    real_set_var = real_set_df['Portfolio']*InitialInvestment*-1
    # print(VaR_test_list)
    
    error_count = (real_set_var >= VaR_prediction_list).sum()
    # print(error_count)

    error_rate = (error_count/real_set_var.shape[0])
    # print(f'error rate = {round(error_rate*100,2)}%')

    return error_rate 

# @ Testing section for Historical Simulation method

# *cal VaR function for Historical Simulation method
def cal_VaR_HS(testing_set,method,portfolio_weights=np.array([1])):
    stock_object = method(testing_set,portfolio_weights)
    VaR = (stock_object.Calculating_VaR_by_Historical_Simulation(confidence_level))
    hVaR = stock_object.quantile_to_VaR(VaR,Time,InitialInvestment)
    
    return(hVaR)

def test_stress_testing_historical_simulation_single_stock_200():
    back_test_result = stress_test_function(cal_VaR_by_Historical_Simulation,cal_VaR_HS,AAPL_201day_data)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_stress_testing_historical_simulation_portfolio_200():
    back_test_result = stress_test_function(cal_VaR_by_Historical_Simulation,cal_VaR_HS,portfolio_stock_data_201day,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_stress_testing_historical_simulation_single_stock_1000():
    back_test_result = stress_test_function(cal_VaR_by_Historical_Simulation,cal_VaR_HS,AAPL_1001day_data)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_stress_testing_historical_simulation_portfolio_1000():
    back_test_result = stress_test_function(cal_VaR_by_Historical_Simulation,cal_VaR_HS,portfolio_stock_data_1001day,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05
    
# @ Testing section for parametric method
# * method 1 
def cal_VaR_PM_1(testing_set,method,portfolio_weights=np.array([1])):
    stock_object = method(testing_set,portfolio_weights)
    VaR = (stock_object.Calculating_VaR_by_parametric_method(confidence_level,Time,InitialInvestment))
    
    return(VaR)

def test_stress_testing_parametric_method_1_single_stock_200():
    back_test_result = stress_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_1,AAPL_201day_data)
    print(back_test_result)
    assert back_test_result <= 0.05
    
def test_stress_testing_parametric_method_1_portfolio_200():
    back_test_result = stress_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_1,portfolio_stock_data_201day,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_stress_testing_parametric_method_1_single_stock_1000():
    back_test_result = stress_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_1,AAPL_1001day_data)
    print(back_test_result)
    assert back_test_result <= 0.05
    
def test_stress_testing_parametric_method_1_portfolio_1000():
    back_test_result = stress_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_1,portfolio_stock_data_1001day,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05
    
# * method 2 
def cal_VaR_PM_2(testing_set,method):
    stock_object = method(testing_set,portfolio_weights)
    VaR = (stock_object.Calculating_VaR_by_parametric_method_portfolio(confidence_level,Time,InitialInvestment))
    
    return(VaR)

def test_stress_testing_parametric_method_2_single_stock_200():
    back_test_result = stress_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_2,AAPL_201day_data)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_stress_testing_parametric_method_2_portfolio_200():
    back_test_result = stress_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_2,portfolio_stock_data_201day,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_stress_testing_parametric_method_2_single_stock_1000():
    back_test_result = stress_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_2,AAPL_1001day_data)
    print(back_test_result)
    assert back_test_result <= 0.05
    
def test_stress_testing_parametric_method_2_portfolio_1000():
    back_test_result = stress_test_function(cal_VaR_by_parametric_method,cal_VaR_PM_2,portfolio_stock_data_1001day)
    print(back_test_result)
    assert back_test_result <= 0.05

# @ Testing section for Monte Carlo Simulation method

# * method 1
def cal_VaR_MS_1(testing_set,method,portfolio_weights=np.array([1])):
    stock_object = method(testing_set,portfolio_weights)
    pdp = stock_object.predict_daily_price(501,1000)
    pdp_df_dict = stock_object.combine_the_predict_price(pdp)
    VaR , CVaR = (stock_object.using_HS_to_get_var(pdp_df_dict,Time,InitialInvestment,5))
    
    return VaR

def test_stress_testing_monte_carlo_simulation_method_1_single_stock_200():
    back_test_result = stress_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_1,AAPL_201day_data)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_stress_testing_monte_carlo_simulation_method_1_portfolio_200():
    back_test_result = stress_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_1,portfolio_stock_data_201day,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_stress_testing_monte_carlo_simulation_method_1_single_stock_1000():
    back_test_result = stress_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_1,AAPL_1001day_data)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_stress_testing_monte_carlo_simulation_method_1_portfolio_1000():
    back_test_result = stress_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_1,portfolio_stock_data_1001day,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05

# * method 2
def cal_VaR_MS_2(testing_set,method,portfolio_weights=np.array([1])):
    stock_object = method(testing_set,portfolio_weights)
    pdp = stock_object.predict_daily_price_cholesky_decomposition(501,1000)
    pdp_df_dict = stock_object.combine_the_predict_price(pdp)
    VaR , CVaR = (stock_object.using_HS_to_get_var(pdp_df_dict,Time,InitialInvestment,5))
    
    return VaR

def test_stress_testing_monte_carlo_simulation_method_2_single_stock_200():
    back_test_result = stress_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_2,AAPL_201day_data)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_stress_testing_monte_carlo_simulation_method_2_portfolio_200():
    back_test_result = stress_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_2,portfolio_stock_data_201day,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_stress_testing_monte_carlo_simulation_method_2_single_stock_1000():
    back_test_result = stress_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_2,AAPL_1001day_data)
    print(back_test_result)
    assert back_test_result <= 0.05

def test_stress_testing_monte_carlo_simulation_method_2_portfolio_1000():
    back_test_result = stress_test_function(cal_VaR_by_Monte_Carlo_Simulation_method,cal_VaR_MS_2,portfolio_stock_data_1001day,portfolio_weights)
    print(back_test_result)
    assert back_test_result <= 0.05