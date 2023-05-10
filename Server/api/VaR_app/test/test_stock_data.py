import datetime as dt
import os
import sys

import pandas as pd
import yfinance as yf

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from Stock_data.Get_the_stock_data import *

US_STOCK_LIST = ["TSM","GOOGL","TSLA","MSFT","AAPL"]

#* Test list_to_string_with_space function 
def test_list_to_string_with_space():
    assert list_to_string_with_space(["A","B"]) == "A B"

# * Test Get_the_time_frame function
def test_Get_the_time_frame():
    assert (isinstance(Get_the_time_frame(10),dt.date)) 

#* Test create_stock_object function 
def test_create_stock_object():
    assert (isinstance(create_stock_object(["TSLA"]),yf.tickers.Tickers)) 

#* test Get_the_single_stock_historical_data_in_the_given_time
def test_Get_the_single_stock_historical_data_in_the_given_time():
    assert (isinstance(Get_the_single_stock_historical_data_in_the_given_time("TSLA",100),pd.DataFrame))


# * test_create_stock_object_for_portfolio
def test_create_stock_object_for_portfolio():
    assert (isinstance(create_stock_object(US_STOCK_LIST),yf.tickers.Tickers)) 


# * test the function is that getting the correct stock portfolio
def test_Get_the_stock_portfolio_historical_data_in_the_given_time():
    assert (isinstance(Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,100),pd.DataFrame))

def test_Get_the_stock_portfolio_historical_data_in_the_given_time2():

    df = Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,100)

    ticket = sorted(df.columns.values.tolist())
    assert ticket == sorted(US_STOCK_LIST)


def test_check_stock_exists_single():
    flag,wrong_list_return = check_stock_exists(["AAPL"])
    assert flag == True 
    
def test_check_stock_exists_single_list():
    flag,wrong_list_return = check_stock_exists(["AAPL"])
    assert len(wrong_list_return) == 0 

def test_check_stock_exists():
    flag,wrong_list_return = check_stock_exists(US_STOCK_LIST)
    assert flag == True
    
def test_check_stock_exists_list():
    flag,wrong_list_return = check_stock_exists(US_STOCK_LIST)
    assert len(wrong_list_return) == 0 
    
def test_check_stock_exists_2_single():
    wrong_list = ["ABCDE"]
    flag,wrong_list_return = check_stock_exists(wrong_list)
    assert flag == False
    
def test_check_stock_exists_2_single_list():
    wrong_list = ["ABCDE"]
    flag,wrong_list_return = check_stock_exists(wrong_list)
    assert wrong_list_return == "ABCDE"
    
def test_check_stock_exists_2():
    wrong_list = ["TSM","ABCDE","ABCDE","MSFT","AAPL"]
    flag,wrong_list_return = check_stock_exists(wrong_list)
    assert flag == False

def test_check_stock_exists_2_list():
    wrong_list = ["TSM","ABCDE","ABCDEF","MSFT","AAPL"]
    flag,wrong_list_return = check_stock_exists(wrong_list)
    assert wrong_list_return == "ABCDE ABCDEF"
    
def test_check_weight():
    flag = check_weight(US_STOCK_LIST,[0.2,0.15,0.15,0.3,0.2])
    assert flag == True
    
def test_check_weight2():
    """check the sum of weight
    """
    flag = check_weight(US_STOCK_LIST,[0.2,0.15,0.15,0.3,0.1])
    assert flag == False

def test_check_weight3():
    """check the length is same for both list 
    """
    flag = check_weight(US_STOCK_LIST,[0.2,0.15,0.15,0.3,0.2,0.2])
    assert flag == False
    