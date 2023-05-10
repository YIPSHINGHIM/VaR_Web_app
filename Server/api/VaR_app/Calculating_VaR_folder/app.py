import datetime
import json
import os
import random
import sys
from pprint import pprint

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import yfinance as yf
from rest_framework import status
from rest_framework.response import Response
from scipy.stats import norm, t

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import numpy as np

if __name__ == "__main__":
    print("under main")
    print("running app.py in VaR_app folder")
    from Calculating_VaR import (Historical_Simulation,
                                 Monte_Carlo_Simulation_method, OptionVaR,
                                 cal_option_price, data_initialise,
                                 parametric_method)
    
else:
    print("not run under main")

    from .Calculating_VaR import (Historical_Simulation,
                             Monte_Carlo_Simulation_method, data_initialise,
                             parametric_method,cal_option_price,OptionVaR)

from Stock_data import Get_the_stock_data


# @ For API ---------------------------------------------------------------------------
def check_user_input(data):
    flag = True
    
    # period
    try:
        period = int(data['period'])
    except ValueError:
        print("period ("+data['period']+") cannot convert to int")
        flag = False
        return flag,Response("period ("+data['period']+") cannot convert to int" ,status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # Time
    try:
        Time = int(data['Time'])
    except ValueError:
        print("Time ("+data['Time']+") cannot convert to int")
        flag = False
        return flag,Response("Time cannot convert to int",status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # InitialInvestment
    try:
        InitialInvestment = float(data['InitialInvestment'])
    except ValueError:
        print("InitialInvestment ("+data['InitialInvestment']+") cannot convert to float")
        flag = False
        return flag,Response("InitialInvestment cannot convert to float",status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # Stock list convert 
    try:
        temp = data['stock_list']
        # if type(temp) == list :
            # stock_list = data['stock_list']
        # else:
        stock_list = data['stock_list'].split(",")
        
    except ValueError:
        print("given the wrong input in stock list , please send again")
        flag = False
        return flag,Response("given the wrong input in stock list , please send again",status=status.HTTP_406_NOT_ACCEPTABLE)
    
    check_stock_flag = False
    check_stock_flag,wrong_stock_list = Get_the_stock_data.check_stock_exists(stock_list)
    if type(stock_list) == list and check_stock_flag:
        print("all correct not action require")
    else:
        print(f"Error, given the wrong ticker : {wrong_stock_list}")
        flag = False
        return flag,Response(f"Error, given the wrong ticker : {wrong_stock_list}",status=status.HTTP_406_NOT_ACCEPTABLE)
    
    # portfolio_weights convert
    try:
        temp = data['portfolio_weights']
        # if type(temp) == list :
            # portfolio_weights_str = data['portfolio_weights']
        # else:            
        portfolio_weights_str = data['portfolio_weights'].split(",")
        portfolio_weights = [float(i) for i in portfolio_weights_str]
        
    except ValueError:
        print("given the wrong input in portfolio weights , please send again")
        flag = False
        return flag,Response("given the wrong input in portfolio weights , please send again",status=status.HTTP_406_NOT_ACCEPTABLE)
    
    check_weight_list_flag = False
    check_weight_list_flag = Get_the_stock_data.check_weight(stock_list,portfolio_weights)
    
    if check_weight_list_flag :
        print("all correct not action require")
    else:
        print("Error, given portfolio weights not match with stock list provide or portfolio weights add up not equal to 1")
        flag = False
        return flag,Response("Error, given portfolio weights not match with stock list provide or portfolio weights add up not equal to 1",status=status.HTTP_406_NOT_ACCEPTABLE)
    
    try:
        confidence_level = float(data['confidence_level'])
    except ValueError:
        print("confidence_level ("+data['confidence_level']+") cannot convert to float")
        flag = False
        return flag,Response("confidence_level cannot convert to float",status=status.HTTP_406_NOT_ACCEPTABLE)
    
    return flag,Response("data received , will do the simulation now")

def make_clean_data(data):
    period = int(data.period)
    Time = int(data.Time)
    InitialInvestment = float(data.InitialInvestment)
    stock_list = data.stock_list.split(",")
    print(stock_list)
    print(type(data.stock_list))
    portfolio_weights_str = data.portfolio_weights_str.split(",")
    print(portfolio_weights_str)
    portfolio_weights = [float(i) for i in portfolio_weights_str]
    confidence_level = float(data.confidence_level)
    
    clean_data_data = {
        'Data_id':data.Data_id,
        'period' : period,
        'Time' :Time,    
        'InitialInvestment':InitialInvestment,
        'stock_list':stock_list,
        'portfolio_weights':portfolio_weights,
        'confidence_level':confidence_level
}
    
    return clean_data_data

def unixtime2timestamp(json_data):
    data = json.loads(json_data)

    for key, value in data.items():
        new_value = {}
        for timestamp, val in value.items():
            timestamp = int(timestamp) / 1000
            date = datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            new_value[date] = val
        data[key] = new_value

    temp_json = json.dumps(data)
    return(temp_json)

def pd_to_json(data):
    
    period = data['period']
    US_STOCK_LIST = data['stock_list']
    portfolio_weights = np.array(data['portfolio_weights'])
    

    portfolio_stock_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)
    
    

    portfolio_stock_object = data_initialise(Stock_historical_data_df = portfolio_stock_data,portfolio_weights=portfolio_weights)
    
    portfolio_returns =portfolio_stock_object.Calculating_daily_portfolio_Returns()
     
    
    # print(portfolio_stock_data)
    portfolio_stock_data_json = portfolio_stock_data.to_json()
    # pprint(portfolio_stock_data_json)
    
    portfolio_stock_data_json_timeStamp = unixtime2timestamp(portfolio_stock_data_json)
    
    # print(portfolio_returns)
    portfolio_returns_json = portfolio_returns.to_json()
    portfolio_returns_json_timeStamp = unixtime2timestamp(portfolio_returns_json)

    
    return (portfolio_stock_data_json_timeStamp,portfolio_returns_json_timeStamp)

def check_Option_user_input(data):
    flag = True

    # stock_list
    try:
        stock_list = data['stock_list'].split(",")
        # print(stock_list)
    except ValueError:
        print("given the wrong input in stock list, please send again")
        flag = False
        return flag, Response("given the wrong input in stock list, please send again", status=status.HTTP_406_NOT_ACCEPTABLE)

    # option_type
    try:
        option_type = data['option_type'].split(",")
        if not all(t.lower() in ['call', 'put'] for t in option_type):
            raise ValueError
    except ValueError:
        print("given the wrong input in option_type, please send again")
        flag = False
        return flag, Response("given the wrong input in option_type, please send again", status=status.HTTP_406_NOT_ACCEPTABLE)

    # strike_price
    try:
        strike_price = [float(x) for x in data['strike_price'].split(",")]
    except ValueError:
        print("given the wrong input in strike_price, please send again")
        flag = False
        return flag, Response("given the wrong input in strike_price, please send again", status=status.HTTP_406_NOT_ACCEPTABLE)

    # expiration_date
    try:
        expiration_date = [datetime.datetime.strptime(x, '%Y-%m-%d') for x in data['expiration_date'].split(",")]
    except ValueError:
        print("given the wrong input in expiration_date, please send again")
        flag = False
        return flag, Response("given the wrong input in expiration_date, please send again", status=status.HTTP_406_NOT_ACCEPTABLE)

    # portfolio_weights
    try:
        portfolio_weights = [float(x) for x in data['portfolio_weights'].split(",")]
    except ValueError:
        print("given the wrong input in portfolio_weights, please send again")
        flag = False
        return flag, Response("given the wrong input in portfolio_weights, please send again", status=status.HTTP_406_NOT_ACCEPTABLE)

    # risk_free_rate
    try:
        risk_free_rate = float(data['risk_free_rate'])
    except ValueError:
        print("risk_free_rate (" + data['risk_free_rate'] + ") cannot convert to float")
        flag = False
        return flag, Response("risk_free_rate cannot convert to float", status=status.HTTP_406_NOT_ACCEPTABLE)

    # confidence_level
    try:
        confidence_level = float(data['confidence_level'])
    except ValueError:
        print("confidence_level (" + data['confidence_level'] + ") cannot convert to float")
        flag = False
        return flag, Response("confidence_level cannot convert to float", status=status.HTTP_406_NOT_ACCEPTABLE)

    # number_of_options
    try:
        number_of_options = [int(x) for x in data['number_of_options'].split(",")]
    except ValueError:
        print("given the wrong input in number_of_options, please send again")
        flag = False
        return flag, Response("given the wrong input in number_of_options, please send again", status=status.HTTP_406_NOT_ACCEPTABLE)

    return flag, Response("data received, will do the simulation now")

def make_clean_option_data(data):
    stock_list = data['stock_list'].split(",")
    option_type = data['option_type'].split(",")
    strike_price = [float(x) for x in data['strike_price'].split(",")]
    expiration_date = data['expiration_date'].split(",")
    portfolio_weights = [float(x) for x in data['portfolio_weights'].split(",")]
    risk_free_rate = float(data['risk_free_rate'])
    confidence_level = float(data['confidence_level'])
    number_of_options = [int(x) for x in data['number_of_options'].split(",")]

    clean_option_data = {
        'stock_list': stock_list,
        'option_type': option_type,
        'strike_price': strike_price,
        'expiration_date': expiration_date,
        'portfolio_weights': portfolio_weights,
        'risk_free_rate': risk_free_rate,
        'confidence_level': confidence_level,
        'number_of_options': number_of_options
    }

    return clean_option_data

def check_Stock_user_input(data):
    flag = True

    # period
    try:
        period = int(data['period'])
    except ValueError:
        print("period (" + data['period'] + ") cannot convert to int")
        flag = False
        return flag, Response("period (" + data['period'] + ") cannot convert to int", status=status.HTTP_406_NOT_ACCEPTABLE)

    # Time
    try:
        Time = int(data['Time'])
    except ValueError:
        print("Time (" + data['time'] + ") cannot convert to int")
        flag = False
        return flag, Response("Time cannot convert to int", status=status.HTTP_406_NOT_ACCEPTABLE)

    # InitialInvestment
    try:
        InitialInvestment = float(data['InitialInvestment'])
    except ValueError:
        print("InitialInvestment (" + data['initialInvestment'] + ") cannot convert to float")
        flag = False
        return flag, Response("InitialInvestment cannot convert to float", status=status.HTTP_406_NOT_ACCEPTABLE)

    # Stock list convert
    try:
        stock_list = data['stock_list'].split(",")
    except ValueError:
        print("given the wrong input in stock list, please send again")
        flag = False
        return flag, Response("given the wrong input in stock list, please send again", status=status.HTTP_406_NOT_ACCEPTABLE)

    check_stock_flag, wrong_stock_list = Get_the_stock_data.check_stock_exists(stock_list)
    if check_stock_flag:
        print("all correct, not action required")
    else:
        print(f"Error, given the wrong ticker: {wrong_stock_list}")
        flag = False
        return flag, Response(f"Error, given the wrong ticker: {wrong_stock_list}", status=status.HTTP_406_NOT_ACCEPTABLE)

    # portfolio_weights convert
    try:
        portfolio_weights_str = data['portfolio_weights'].split(",")
        portfolio_weights = [float(i) for i in portfolio_weights_str]
    except ValueError:
        print("given the wrong input in portfolio weights, please send again")
        flag = False
        return flag, Response("given the wrong input in portfolio weights, please send again", status=status.HTTP_406_NOT_ACCEPTABLE)

    check_weight_list_flag = Get_the_stock_data.check_weight(stock_list, portfolio_weights)

    if check_weight_list_flag:
        print("all correct, not action required")
    else:
        print("Error, given portfolio weights not match with stock list provided or portfolio weights add up not equal to 1")
        flag = False
        return flag, Response("Error, given portfolio weights not match with stock list provided or portfolio weights add up not equal to 1", status=status.HTTP_406_NOT_ACCEPTABLE)

    try:
        confidence_level = float(data['confidence_level'])
    except ValueError:
        print("confidence_level (" + data['confidence_level'] + ") cannot convert to float")
        flag = False
        return flag, Response("confidence_level cannot convert to float", status=status.HTTP_406_NOT_ACCEPTABLE)

    return flag, Response("data received, will do the simulation now")


# @ For VaR ---------------------------------------------------------------------------
# @ Historical Simulation
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# * portfolio historical simulation method
def historical_simulation_portfolio(data):
    # * Testing for portfolio

    period = data['period']
    Time = data['Time']
    InitialInvestment = data['InitialInvestment']
    US_STOCK_LIST = data['stock_list']
    portfolio_weights = np.array(data['portfolio_weights'])
    confidence_level = data['confidence_level']
    
    portfolio_stock_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)

    portfolio_stock_object = Historical_Simulation(Stock_historical_data_df = portfolio_stock_data,portfolio_weights=portfolio_weights)


    VaR = portfolio_stock_object.Calculating_VaR_by_Historical_Simulation(confidence_level)

    CVaR = portfolio_stock_object.Calculating_CVaR_by_Historical_Simulation(confidence_level)

    hVaR = portfolio_stock_object.quantile_to_VaR(VaR,Time,InitialInvestment)

    hCVaR = portfolio_stock_object.quantile_to_VaR(CVaR,Time,InitialInvestment)

 
    
    print('Historical_Simulation_portfolio')

    print(f'For portfolio : {US_STOCK_LIST}')
    print(f'weight : {portfolio_weights}')
    print('Value at Risk 95th CI    :      ', round(hVaR,2))
    print('Conditional VaR 95th CI  :      ', round(hCVaR,2))
    # hVaR = 1
    
    return_data = {
        'hVaR' : hVaR,
        'hCVaR':hCVaR,
        'InitialInvestment':InitialInvestment
    }
    
    return return_data

# @ Model building 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# * portfolio model build method 1
def parametric_method_one_portfolio(data):

    period = data['period']
    Time = data['Time']
    InitialInvestment = data['InitialInvestment']
    US_STOCK_LIST = data['stock_list']
    portfolio_weights = np.array(data['portfolio_weights'])
    confidence_level = data['confidence_level']

    portfolio_stock_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)

    portfolio_stock_object = parametric_method(portfolio_stock_data,portfolio_weights)


    VaR =(portfolio_stock_object.Calculating_VaR_by_parametric_method(confidence_level,Time,InitialInvestment))

    print('The first parametric (model build) method for calculating the portfolio VaR ')
    print(f'For single stock : {US_STOCK_LIST}')
    print('Value at Risk 95th CI    :      ', round(VaR,2))
    
    return_data = {
        'hVaR' : VaR,
        'InitialInvestment':InitialInvestment
    }
    
    return return_data

# * portfolio model build method 2
def parametric_method_two_portfolio(data):
    
    period = data['period']
    Time = data['Time']
    InitialInvestment = data['InitialInvestment']
    US_STOCK_LIST = data['stock_list']
    portfolio_weights = np.array(data['portfolio_weights'])
    confidence_level = data['confidence_level']

    portfolio_stock_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)

    portfolio_stock_object = parametric_method(portfolio_stock_data,portfolio_weights)

    VaR =(portfolio_stock_object.Calculating_VaR_by_parametric_method_portfolio(confidence_level,Time,InitialInvestment))
    # print(VaR)

    print('The second parametric (model build) method for calculating the portfolio VaR')
    print(f'For single stock : {US_STOCK_LIST}')
    print('Value at Risk 95th CI    :      ', round(VaR,2))

    return_data = {
        'hVaR' : VaR, 
    }
    
    return return_data

# @ Monte Carlo Simulation 
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
def Monte_Carlo_Simulation_method_one_portfolio(data):
    
    period = data['period']
    Time = data['Time']
    InitialInvestment = data['InitialInvestment']
    US_STOCK_LIST = data['stock_list']
    portfolio_weights = np.array(data['portfolio_weights'])
    confidence_level = data['confidence_level']

    portfolio_stock_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)

    # print(portfolio_stock_data.head())

    portfolio_stock_object = Monte_Carlo_Simulation_method(portfolio_stock_data,portfolio_weights)

    # day , time
    pdp = portfolio_stock_object.predict_daily_price(period,period*2 -2)
    # print(pdp)
    
    pdp_df_dict = portfolio_stock_object.combine_the_predict_price(pdp)
    # print(pdp_df_dict)
    
    VaR , CVaR = (portfolio_stock_object.using_HS_to_get_var(pdp_df_dict,Time,InitialInvestment,confidence_level))
    
    print('Monte Carlo Simulation method one portfolio')


    print(f'For portfolio : {US_STOCK_LIST}')
    print(f'weight : {portfolio_weights}')
    print('Value at Risk 95th CI    :      ', round(VaR,2))
    print('Conditional VaR 95th CI  :      ', round(CVaR,2))
    
    return_data = {
        'hVaR' : VaR,
        'hCVaR':CVaR,
        'InitialInvestment':InitialInvestment
        
    }
    
    return return_data
    
def Monte_Carlo_Simulation_method_two_portfolio(data):
    
    period = data['period']
    Time = data['Time']
    InitialInvestment = data['InitialInvestment']
    US_STOCK_LIST = data['stock_list']
    portfolio_weights = np.array(data['portfolio_weights'])
    confidence_level = data['confidence_level']

    # print(US_STOCK_LIST)
    portfolio_stock_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)
    
    

    portfolio_stock_object = Monte_Carlo_Simulation_method(portfolio_stock_data,portfolio_weights)
    
    # period,iterations
    pdp = portfolio_stock_object.predict_daily_price_cholesky_decomposition(period,period*2 -2)
    # print(pdp)
    
    pdp_df_dict = portfolio_stock_object.combine_the_predict_price(pdp)
    # print(pdp_df_dict)
    
    VaR , CVaR = (portfolio_stock_object.using_HS_to_get_var(pdp_df_dict,Time,InitialInvestment,confidence_level))
    
    print('Monte Carlo Simulation method two portfolio')

    print(f'For portfolio : {US_STOCK_LIST}')
    print(f'weight : {portfolio_weights}')
    print('Value at Risk 95th CI    :      ', round(VaR,2))
    print('Conditional VaR 95th CI  :      ', round(CVaR,2))
    
    return_data = {
        'hVaR' : VaR,
        'hCVaR':CVaR,
        'InitialInvestment':InitialInvestment
        
    }
    
    return return_data

# @ For Option ---------------------------------------------------------------------------

def option_VaR_single(data):

    portfolio_stock_object = cal_option_price("AAPL","call",180,pd.Timestamp('2023-06-30'),0.05)
    
    print(portfolio_stock_object)
     
    print(portfolio_stock_object.option_type)
    sigma = portfolio_stock_object.cal_sigma()["AAPL"]
    print(f'sigma = {sigma}' )
    
    d1,d2 = (portfolio_stock_object.cal_d1_d2(152.54,sigma,0))
    print(f'd1 = {d1} , d2 = {d2}')
    
    option_price = (portfolio_stock_object.black_scholes(152.54,sigma,0))
    print(f'option_price = {option_price}')
    
    day_to_maturity = (pd.Timestamp('2023-06-30') - pd.Timestamp.today()).days
    
    print((day_to_maturity))
    
    option_prices = []
    market_price = []
    
    for i in range(0,day_to_maturity-1):
        # TODO , we can use historical data to replace the random 
        S = (random.uniform(162, 198)) 
        market_price.append(S)
        option_price = (portfolio_stock_object.black_scholes(S,sigma,i))
        option_prices.append(option_price)
    
    print("Market price list")
    print(market_price)
    
    print("option price list")
    print(option_prices)
    print(len(option_prices))
    
    print("option price returns list")
    option_price_returns = []
    for i in range(0,len(option_prices)):
        if i < (len(option_prices) - 1):
            option_price_return = option_prices[i+1] - option_prices[i]
            option_price_returns.append(option_price_return)
        
    print("length of option price")
    print(len(option_price_returns))
    print(option_price_returns)
    
    # TODO we sort the list we can get the VaR 
    VaR_95 = np.percentile(option_price_returns,95)   
    # print(VaR_95) 
    
    return VaR_95

def option_portfolio_var(data):
    # Initialize the input parameters
    US_STOCK_LIST = data['stock_list']
    option_type = data['option_type']
    strike_price = data['strike_price']
    expiration_date = data['expiration_date']
    portfolio_weights = data['portfolio_weights']
    risk_free_rate = data['risk_free_rate']    
    confidence_level = data['confidence_level']
    number_of_options = data['number_of_options']
    
    options = []
    
    for i in range(len(US_STOCK_LIST)):
        options.append(
            {"ticker": US_STOCK_LIST[i], 
             "option_type": option_type[i], 
             "strike_price": strike_price[i], 
             "expiration_date": pd.Timestamp(expiration_date[i]), 
             "risk_free_rate": risk_free_rate, 
             }
            )

    all_option_price_returns = []
    
    for index, option_data in enumerate(options):
        option = cal_option_price(**option_data)
        weight = portfolio_weights[index]
        num_options = number_of_options[index]
        sigma = option.cal_sigma()[option.ticker]
        day_to_maturity = (option.expiration_date - pd.Timestamp.today()).days
        temp_df = option.Stock_historical_data_df.tail(day_to_maturity).copy()
        
        option_prices = []

        for i in range(0, day_to_maturity-1):
            S = temp_df[option.ticker].iloc[i]
            option_price = (option.black_scholes(S, sigma, i))
            option_prices.append(option_price)

        option_price_returns = [(option_prices[i+1] - option_prices[i]) * weight * num_options for i in range(len(option_prices) - 1)]
        all_option_price_returns.extend(option_price_returns)

    portfolio_VaR = np.percentile(all_option_price_returns, 100 - confidence_level)

    for keys, value in data.items():
        print(f"{keys} : {value}")
        
    print(f"Value at Risk 95th CI    :       {portfolio_VaR}")
    
    return portfolio_VaR

def option_HS_var(data):
    option_var = OptionVaR(options_data=data,confidence_level=data['confidence_level'])

    portfolio_VaR = option_var.calculate_var()

    for keys, value in data.items():
        print(f"{keys} : {value}")

    print(f"Value at Risk 95th CI    :       {portfolio_VaR}")

    return portfolio_VaR

def option_MS_var(option_data):
        
    period = 501
    US_STOCK_LIST = option_data['stock_list']
    portfolio_weights = np.array(option_data['portfolio_weights'])

    portfolio_stock_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,period)

    portfolio_stock_object = Monte_Carlo_Simulation_method(portfolio_stock_data,portfolio_weights)
    
    # period,iterations #TODO change back to 1000
    
    pdp = portfolio_stock_object.predict_daily_price_cholesky_decomposition(period,100)
    # print(pdp)
    
    simulated_stock_prices = portfolio_stock_object.combine_the_predict_price(pdp)
    
    # Calculate VaR using Monte Carlo simulated stock prices
    all_MS_VaR = []
    
    for keys, value in simulated_stock_prices.items():
        
        option_var_monte_carlo = OptionVaR(
            options_data=option_data,
            confidence_level=option_data['confidence_level'],
            simulated_stock_prices=value
        )
        
        portfolio_VaR_monte_carlo = option_var_monte_carlo.calculate_var_monte_carlo()

        all_MS_VaR.append(portfolio_VaR_monte_carlo)
        print(f"finished {keys}")
    
    # print(all_MS_VaR)
    
    portfolio_VaR = np.percentile(all_MS_VaR, 100 - option_data['confidence_level'])
    
    print(f"final Value at Risk 95th CI    :       {portfolio_VaR}")
        
    return portfolio_VaR


if __name__ == "__main__":
    
    period = 501
    Time = 1
    InitialInvestment = 10000
    
    Portfolio_data = {
        'period':period,
        'Time' : Time,
        'InitialInvestment' : 10000,
        'stock_list': ["TSM","GOOGL","TSLA","MSFT","AAPL"],
        'portfolio_weights' :[0.2,0.15,0.15,0.3,0.2],
        'confidence_level':5
    }
    
    Single_data = {
        'period':period,
        'Time' : Time,
        'InitialInvestment' : InitialInvestment,
        'stock_list': ["AAPL"],
        'portfolio_weights' :[1],
        'confidence_level':5
    }
    
    option_Single_data = {
        'stock_list': ["AAPL"],
        'option_type':["call"],
        'strike_price':[140],
        'expiration_date':['2023-06-30'],
        'portfolio_weights' :[1],
        'risk_free_rate':0.05,
        'confidence_level':5,
        'number_of_options': [100]
    }
    
    option_Portfolio_data = {
        'stock_list': ["AAPL","TSM","MSFT"],
        'option_type':["call","put","put"],
        'strike_price':[140,100,300],
        'expiration_date':['2023-06-30','2023-07-30','2023-08-30'],
        'portfolio_weights' :[0.5,0.3,0.2],
        'risk_free_rate':0.05,
        'confidence_level':5,
        'number_of_options': [100, 150, 200]
    }

    print("under main")
    print("running app.py in VaR_app folder")

    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # * driver code to print the result 

    print()
    print('For testing purpose : ')
    print(f'we will use {period} day data ')
    print(f'set the Initial Investment money to {InitialInvestment} USD')
    print(f'Time Horizon will be {Time} day')
    print('and return 95% VaR')
    print('--------------------------------------')


    # # @ Historical Simulation
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # * single stock Historical simulation method 
    # historical_simulation_portfolio(Single_data)
    # print()
    # print('--------------------------------------')

    # # # * portfolio Historical simulation method 
    # historical_simulation_portfolio(Portfolio_data)
    # print()
    # print('--------------------------------------')

    # # @ Model building 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # * single stock model build method 1 
    # parametric_method_one_portfolio(Single_data)
    # print()
    # print('--------------------------------------')

    # # # * portfolio model build method 1
    # parametric_method_one_portfolio(Portfolio_data)
    # print()
    # print('--------------------------------------')

    # # * single stock model build method 2
    # parametric_method_two_portfolio(Single_data)
    # print()
    # print('--------------------------------------')

    # # * portfolio model build method 2
    # parametric_method_two_portfolio(Portfolio_data)
    # print()
    # print('--------------------------------------')

    # # @ Monte Carlo Simulation 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    # # * single stock Monte Carlo simulation method 1
    # Monte_Carlo_Simulation_method_one_portfolio(Single_data)
    # print()
    # print('--------------------------------------')
    
    # # * portfolio Monte Carlo simulation method 1
    # Monte_Carlo_Simulation_method_one_portfolio(Portfolio_data)
    # print()
    # print('--------------------------------------')
    
    # # * single stock Monte Carlo simulation method 2
    # Monte_Carlo_Simulation_method_two_portfolio(Single_data)
    # print()
    # print('--------------------------------------')

    # # # * portfolio Monte Carlo simulation method 2
    # Monte_Carlo_Simulation_method_two_portfolio(Portfolio_data)
    # print()
    # print('--------------------------------------')
        
        
    # @ option VaR
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    
    # * Historical option VaR
    print(option_HS_var(option_Single_data))
    print()
    print('--------------------------------------')
    
    print(option_HS_var(option_Portfolio_data))
    print()
    print('--------------------------------------')

    # * Monte Carlo simulation option VaR
    print(option_MS_var(option_data=option_Single_data))
    print()
    print('--------------------------------------')
    
    print(option_MS_var(option_data=option_Portfolio_data))
    print()
    print('--------------------------------------')
    
else:
   print("not under main -> mean call from Django")


    





