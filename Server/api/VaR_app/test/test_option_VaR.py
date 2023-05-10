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


option_data = {
    'stock_list': ["AAPL","TSM","MSFT"],
    'option_type':["call","put","put"],
    'strike_price':[140,100,300],
    'expiration_date':['2023-06-30','2023-07-30','2023-08-30'],
    'portfolio_weights' :[0.5,0.3,0.2],
    'risk_free_rate':0.05,
    'confidence_level':5,
    'number_of_options': [100, 150, 200]
}

optionVaR = Calculating_VaR.OptionVaR
Monte_Carlo_Simulation_method = Calculating_VaR.Monte_Carlo_Simulation_method


def test_calculate_var():
    portfolio_obj = optionVaR(option_data,option_data["confidence_level"])
    
    option_var = portfolio_obj.calculate_var()

    assert isinstance(option_var, float)
    
def test_calculate_var_monte_carlo():
    
    portfolio_stock_object = Monte_Carlo_Simulation_method(portfolio_stock_data_100day,[0.4,0.15,0.15,0.2,0.1])
    
    pdp = portfolio_stock_object.predict_daily_price_cholesky_decomposition(period,100)
    
    simulated_stock_prices = portfolio_stock_object.combine_the_predict_price(pdp)
        
    all_MS_VaR = []
    
    for keys, value in simulated_stock_prices.items():
        
        option_var_monte_carlo = optionVaR(
            options_data=option_data,
            confidence_level=option_data['confidence_level'],
            simulated_stock_prices=value
        )
    
        portfolio_VaR_monte_carlo = option_var_monte_carlo.calculate_var_monte_carlo()
        all_MS_VaR.append(portfolio_VaR_monte_carlo)
        
    portfolio_VaR = np.percentile(all_MS_VaR, 100 - option_data['confidence_level'])

    assert isinstance(portfolio_VaR, float)
