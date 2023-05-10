import datetime as dt

import pandas as pd
import yfinance as yf


def list_to_string_with_space(list:list[str]):
    """
    transfer a list to a string with space

    Parameters
    ----------
    list : list[str]
        A list 

    Returns 
    ----------
    str : 
        concatenate the element in the string    
    """
    
    my_str = ' '.join(list)
    return(my_str)

def Get_the_time_frame(how_many_day:int):
    """Return the date from today to the day given 

    Parameters
    ----------
    how_many_day : int
        how many day user want to get 

    Returns
    -------
    date:
        return the date from today to the previous given days
    """
    
    # getting stock data 
    today = dt.date.today()
    
    historical_data_time_frame = today - dt.timedelta(days=how_many_day)
    # print(today)
    return historical_data_time_frame

# One_hundred_day_before = Get_the_time_frame(100)


def create_stock_object(stock_list:list[str]):
    """Create a stock Object in the yfinance package 

    Parameters
    ----------
    stock_list : list[str]
        A list has all the stock ticket user want to get the historical data 

    Returns
    -------
    Tickers
        The tickers object from yfinance  
    """
    stock_list_str = list_to_string_with_space(stock_list)
    tickers = yf.Tickers(stock_list_str)

    return tickers



def Get_the_single_stock_historical_data_in_the_given_time(stock_ticket:str ,period:int):
    """
    Get the single stock historical data in the given time 

    Parameters
    ----------
    stock_ticket : str
        The stock ticket that user want to get the historical data 
    period : int
        how many day data the user want  

    Returns
    -------
    pd.dataframe
        the historical data in the given time
    """

    Stock_ticket = create_stock_object([stock_ticket])
    closing_price_df = Stock_ticket.tickers[stock_ticket].history(period = f'{period}d')[["Close"]]
    
    return (closing_price_df)



# TSLA_100day_data =  Get_the_single_stock_historical_data_in_the_given_time("TSLA",732)


def Get_the_stock_portfolio_historical_data_in_the_given_time(stock_list:list[str],period:int):
    """
    Get the portfolio closing historical data in the given time 

    Parameters
    ----------
    stock_ticket : list[str]
        The list of stock ticket that user want to get the historical data 
    period : int
        how many day data the user want  

    Returns
    -------
    pd.dataframe
        the historical data in the given time
    """

    portfolio_stock_ticket = create_stock_object(stock_list)
    
    portfolio_closing_price_df = pd.DataFrame
    for ticket_symbol in stock_list:

        single_closing_price_df = portfolio_stock_ticket.tickers[ticket_symbol].history(period=f'{period}d')[['Close']]


        if ticket_symbol == stock_list[0]:
            # print('1st')
            portfolio_closing_price_df = single_closing_price_df.copy()
            portfolio_closing_price_df = portfolio_closing_price_df.rename({'Close' : ticket_symbol},axis='columns')

        else:
            # print(ticket_symbol)
            portfolio_closing_price_df = pd.concat([portfolio_closing_price_df,single_closing_price_df],axis=1)
            portfolio_closing_price_df = portfolio_closing_price_df.rename({'Close' : ticket_symbol},axis='columns')


    # print(portfolio_closing_price_df)

    return portfolio_closing_price_df


def check_stock_exists(stock_list:list[str]):
    """
    This function is to check the given ticket is correct or not to prevent error

    Parameters
    ----------
    stock_list : list[str]
        A stock list user provide 

    Returns
    -------
    flag : 
        return true if everything correct , otherwise return false 
    wrong_ticker_list :
        return the wrong ticker name list 
    
    """
    # print(stock_list)
    flag = True
    wrong_ticker_list = []
    
    for stock in stock_list:
        try:
            yf.Ticker(stock).fast_info.get('currency')
            # print(yf.Ticker(stock).fast_info.get('currency'))
        except KeyError:
            wrong_ticker_list.append(stock)
            flag = False
    
    if wrong_ticker_list:
        wrong_ticker_list = list_to_string_with_space(wrong_ticker_list)
        print(f'Error, given the wrong ticker : {wrong_ticker_list}')
    else:
        print("All ticker symbol correct")
        
    return flag ,wrong_ticker_list


def check_weight(stock_list:list[str],portfolio_weights:list[float]):
    """
    Check do the sum of weight is 1

    Parameters
    ----------
    stock_list : list[str]
        stock list provide by user 
    portfolio_weights : list[float]
        portfolio weight provide by user 

    Returns
    -------
    flag
        return true if weight is correct , false if wrong
    """
    flag = True
    if len(stock_list) != len(portfolio_weights):
        flag = False
    
    sum_of_portfolio_weights = sum(portfolio_weights)
    print(sum_of_portfolio_weights)
    
    if sum_of_portfolio_weights > 1.0 or sum_of_portfolio_weights < 1.0:
        flag = False
        
    return flag
                    

# driver code : 
US_STOCK_LIST = ["TSM","GOOGL","TSLA","MSFT","AAPL"]
wrong_list = ["TSM","ABCD","ABCDE","MSFT","AAPL"]

# Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,501)

# print(Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,501))

# print(check_stock_exists(wrong_list))
# print(check_weight(US_STOCK_LIST,[0.2,0.15,0.15,0.3,0.2]))

# Get_the_stock_portfolio_historical_data_in_the_given_time(US_STOCK_LIST,501).to_csv("temp_portfolio_closing_price_501day.csv")

# portfolio = pd.read_csv('temp_portfolio_closing_price.csv',index_col='Date')
# print(portfolio)

# Get_the_stock_portfolio_historical_data_in_the_given_time(["AAPL"],501).to_csv("temp_AAPL_closing_price_501day.csv")

# AAPL = pd.read_csv('temp_AAPL_closing_price_501day.csv',index_col='Date')
# print(AAPL)
