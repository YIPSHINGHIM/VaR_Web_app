import math
import os
import pathlib
import sys

import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import yfinance as yf
from scipy.stats import norm
from Stock_data import Get_the_stock_data

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class data_initialise:
    """
    This class is used to initialise and manipulate stock data.

    Methods
    -------
    __init__(self, Stock_historical_data_df, portfolio_weights=np.array([1]))
        Initializes the raw data for the stocks.

    portfolioPerformance(self, weights, meanReturns, covMatrix, Time)
        Calculates the portfolio performance.

    Calculating_daily_portfolio_Returns(self)
        Calculates the daily returns for the given stock and closing price.

    add_Portfolio_columns_to_df(self, Stock_historical_data_df_with_returns: pd.DataFrame)
        Using the given weights and historical returns data to create a new column which calls portfolio column.

    quantile_to_VaR(self, quantile: float, Time: int, InitialInvestment: float)
        Returns the VaR from the given quantile.

    plot_graph(self, price_list, stock)
        Plots a graph of the given `price_list` for the `stock`.
    """
    
    # TODO need to put error check here , if is portfolio need to raise error
    def __init__(self, Stock_historical_data_df,portfolio_weights=np.array([1])):
        """
        Constructor

        Parameters
        ----------
        Stock_historical_data_df : pd:dataframe
            A pandas dataframe which has closing price for a specific stock, can be a portfolio or a single stock.
        portfolio_weights : np.array
            An array that contains the weight for different stock, if not given, default is 1.
        """
        
        self.Stock_historical_data_df = Stock_historical_data_df
        self.portfolio_weights = portfolio_weights

    def portfolioPerformance(self,weights, meanReturns, covMatrix, Time):
        """
        Calculates the portfolio performance.

        Parameters
        ----------
        weights: int
            The weights for the portfolio.
        meanReturns : float
            The mean for the returns dataframe.
        covMatrix : pd.dataframe
            This is the covariance matrix for the stock in the list.
        Time: int
            Time horizon.

        Returns
        -------
        tuple
            (returns, std)

        returns :float
            Predicted returns.

        std : float
            Standard deviation.
        """
    
        returns = np.sum(meanReturns*weights)*Time
        std = np.sqrt( np.dot(weights.T, np.dot(covMatrix, weights)) ) * np.sqrt(Time)
        return returns, std

    def Calculating_daily_portfolio_Returns(self):
        """
        Calculates the daily returns for the given stock and closing price.

        Returns
        -------
        pd.dataframe
            A dataframe that has the daily returns for a given stock and closing price.

        """
        portfolio_closing_price_df = self.Stock_historical_data_df.copy()
        # print(portfolio_closing_price_df.columns)

        for ticket_symbol in portfolio_closing_price_df.columns:
            portfolio_closing_price_df[str(ticket_symbol)] = portfolio_closing_price_df[str(ticket_symbol)].pct_change()
            
        portfolio_closing_price_df = portfolio_closing_price_df.dropna()

        return (portfolio_closing_price_df)

    def add_Portfolio_columns_to_df(self,Stock_historical_data_df_with_returns:pd.DataFrame):
        """
        Using the given weights and historical returns data to create a new column which calls portfolio column.

        Parameters
        ----------
        Stock_historical_data_df_with_returns: pd.dataframe
            Historical returns dataframe.

        Returns
        -------
        pd.dataframe
            A dataframe that added a new column call portfolio into the original dataframe.

        """
        temp_df = Stock_historical_data_df_with_returns.copy()

        portfolio_weights = self.portfolio_weights

        # print(portfolio_weights)

        if len(portfolio_weights) == 1:
            # print("only one stock")
            temp_df.rename({f'{temp_df.columns[0]}' : 'Portfolio'},axis=1, inplace=True)

        else:
            temp_df['Portfolio'] = temp_df.dot(portfolio_weights)

        # print(temp_df.head())
        return temp_df
    
    def quantile_to_VaR(self,quantile:float,Time:int,InitialInvestment:float):
        """
        Returns the VaR from the given quantile.

        Parameters
        ----------
        quantile : float
            The quantile for VaR or CVaR.
        Time : int
            Time horizon for the calculation.
        InitialInvestment : float
            Initial investment for your portfolio or stock.

        Returns
        -------
        float
            The VaR for a given portfolio or stock, confidence level, time, and initial investment.
        """

        hVaR = quantile*np.sqrt(Time)

        VaR = InitialInvestment*hVaR
        return VaR*-1
    
    def plot_graph(self,price_list,stock):
        """
        Plots a graph of the given `price_list` for the `stock`.

        Parameters
        ----------
        price_list : list
            A list of prices to be plotted.
        stock : str
            The name of the stock for which the prices are being plotted.

        Returns
        -------
        None
        """

        plt.plot(price_list)
        plt.xlabel('Day')
        plt.ylabel('Price')
        plt.title(stock)
        plt.savefig(f"{pathlib.Path(__file__).resolve().parent.parent}/images/{stock}_MCS.png")
        plt.close()

class Historical_Simulation(data_initialise):
    """
    This class is used to calculate the VaR and CVaR using historical simulation method.

    Methods
    -------
    Calculating_VaR_by_Historical_Simulation(self, confidence_level: int)
        Calculates the VaR using historical simulation method.

    Calculating_CVaR_by_Historical_Simulation(self, confidence_level: int)
        Calculates the CVaR using historical simulation method.
    """

    def Calculating_VaR_by_Historical_Simulation(self ,confidence_level:int):
        """
        Calculates the VaR using historical simulation method.

        Parameters
        ----------
        confidence_level : int
            This is the confidence level for predicting the VaR.

        Returns
        -------
        float
            Percentile of the distribution at the given confidence level.

        Raises
        ------
        TypeError
            If the portfolio return is not a dataframe or series.

        """
        historical_return_df = self.Calculating_daily_portfolio_Returns()
        historical_return_df_with_weight = self.add_Portfolio_columns_to_df(historical_return_df.copy())
        
        portfolio_return = historical_return_df_with_weight["Portfolio"]
        
        if isinstance(portfolio_return,pd.Series):
            # np.sort(Stock_historical_data_df_with_returns.copy())
            return np.percentile(portfolio_return,confidence_level)
        else:
            raise TypeError("Expected returns to be dataframe ot series")

    def Calculating_CVaR_by_Historical_Simulation(self,confidence_level:int):
        """
        Calculates the CVaR using historical simulation method.

        Parameters
        ----------
        confidence_level : int
            This is the confidence level for predicting the CVaR.

        Returns
        -------
        float
            The quantile for CVaR for the given confidence level.

        Raises
        ------
        TypeError
            If the portfolio return is not a dataframe or series.

        """
        historical_return_df = self.Calculating_daily_portfolio_Returns()
        historical_return_df_with_weight = self.add_Portfolio_columns_to_df(historical_return_df.copy())
        
        portfolio_return = historical_return_df_with_weight["Portfolio"]
        
        
        if isinstance(portfolio_return,pd.Series):
            belowVaR = portfolio_return <= self.Calculating_VaR_by_Historical_Simulation(confidence_level)

            # print(Stock_historical_data_df_with_returns[belowVaR].mean())

            return portfolio_return[belowVaR].mean()

        else:
            raise TypeError("Expected returns to be dataframe ot series")
      
class parametric_method(data_initialise):
    """
    This class is used to calculate the VaR using the parametric method.

    Methods
    -------
    Calculating_VaR_by_parametric_method(self, confidence_level: int, Time: int, InitialInvestment: float)
        Calculates the VaR using the parametric method for a single stock or portfolio.

    Calculating_VaR_by_parametric_method_portfolio(self, confidence_level: int, Time: int, InitialInvestment: float)
        Calculates the VaR using the parametric method for a portfolio.

    """
    
    def Calculating_VaR_by_parametric_method(self,confidence_level:int,Time:int,InitialInvestment:float):
        """
        Calculates the VaR using the parametric method for a single stock or portfolio.

        Parameters
        ----------
        confidence_level : int
            Confidence level.

        Time : int
            Time horizon for the calculation.

        InitialInvestment : float
            Initial investment for your portfolio or stock.

        Returns
        -------
        float
            The VaR for given stock, confidence level, time, and initial investment.

        """
        historical_return_df = self.Calculating_daily_portfolio_Returns()
        historical_return_df_with_weight = self.add_Portfolio_columns_to_df(historical_return_df.copy())
        
        Stock_historical_data_df_with_returns = historical_return_df_with_weight.copy()

        # print(Stock_historical_data_df_with_returns)
        # Estimate the average daily return
        mu = np.mean(Stock_historical_data_df_with_returns['Portfolio'])
        # print(mu)
        
        # # Estimate the daily volatility => also = Standard Deviation
        vol = np.std(Stock_historical_data_df_with_returns['Portfolio'])
        # print(vol)

        quantile = norm.ppf(confidence_level/100 , loc = mu,scale =vol)
        # print(type(VaR))

        # scale the quantile with time horizon
        hVaR = self.quantile_to_VaR(quantile,Time,InitialInvestment)
 
        return hVaR

    def Calculating_VaR_by_parametric_method_portfolio(self,confidence_level:int,Time:int,InitialInvestment:float):
        """
        Calculates the VaR using the parametric method for a portfolio.

        Parameters
        ----------
        confidence_level : int
            Confidence level.

        Time : int
            Time horizon for the calculation.

        InitialInvestment : float
            Initial investment for your portfolio or stock.

        Returns
        -------
        float
            The VaR for given portfolio or stock, confidence level, time, and initial investment.

        """
        historical_stock_return = self.Calculating_daily_portfolio_Returns()
        
        Stock_historical_data_df_with_returns = historical_stock_return.copy()
        portfolio_weights = self.portfolio_weights.copy()


        cov_matrix = Stock_historical_data_df_with_returns.copy().cov()
        # print(cov_matrix)

        amount_of_investing_for_each_stock = np.array([i*InitialInvestment for i in portfolio_weights])
        # print(amount_of_investing_for_each_stock)

        i = 0
        
        temp_list = []
        for row,cols in cov_matrix.items():
            # print(f'i = {i} row = {row} ')
            j = 0 
            for col in cols:
                temp_list.append(col*amount_of_investing_for_each_stock[i] * amount_of_investing_for_each_stock[j])
                j+=1
            i+=1

        temp_list = np.array(temp_list)

        sigma = np.sqrt(sum((temp_list)))

        # scale is sigma(standard deviation)
        VaR = norm.ppf(confidence_level/100, scale=sigma) * np.sqrt(Time)
        # print(VaR)

        return VaR*-1

class Monte_Carlo_Simulation_method(data_initialise):
    """
    Class to perform Monte Carlo Simulation.

    Attributes
    ----------
    Stock_historical_data_df : pd.DataFrame
        A pandas dataframe which has closing price for a specific stock, can be a portfolio or a single stock.
    portfolio_weights : np.array
        An array that contains the weight for different stock, if not given, default is 1.

    Methods
    -------
    logarithmic_returns()
        Compute the logarithmic returns of the portfolio or stock.
    compute_drift()
        Compute the drift of the portfolio or stock.
    predict_daily_price(period, iterations)
        Use Monte Carlo Simulation to predict the stock price.
    predict_daily_price_cholesky_decomposition(period, iterations)
        Use Monte Carlo Simulation to predict the stock price using Cholesky decomposition.
    combine_the_predict_price(simulation_result)
        Combine the prediction price data to make it as a DataFrame that we use to do historical simulation.
    using_HS_to_get_var(all_portfolio_prediction, Time, InitialInvestment, confidence_level)
        Uses Historical Simulation to predict the VaR and CVaR for the given portfolio.
    """
    
    # * Compute the logarithmic returns
    def logarithmic_returns(self):
        """
        Compute the logarithmic returns of the portfolio or stock.

        Returns
        -------
        pd.DataFrame
        A pandas DataFrame containing the logarithmic returns for the portfolio or stock.
        """
        daily_return = self.Calculating_daily_portfolio_Returns()
        
        # print(daily_return.head(3))
        
        daily_return = daily_return+1
        # print(daily_return.head(3))
        
        logarithmic_returns_df = daily_return.apply(np.log)
        
        return logarithmic_returns_df

    def compute_drift(self):
        """
        Compute the drift of the portfolio or stock.

        Returns
        -------
        float
            The drift of the portfolio or stock.
        """
        
        log_returns = self.logarithmic_returns()
        # print(log_returns)
        
        u = log_returns.mean()
        var = log_returns.var()
        drift = u - (0.5*var)
        # print(f'u = {u}')
        # print(f'var = {var}')
        # print(f'drift = {drift}')
        
        return drift
    
    def predict_daily_price(self,period,iterations):
        # TODO need to change the pydoc in here
        """
        Use Monte Carlo Simulation to predict the stock price.

        Parameters
        ----------
        period : int
            The time horizon in days for which to predict stock prices.
        iterations : int
            The number of simulations to run for each stock.

        Returns
        -------
        dict
            A dictionary contain the simulation for all the stock provide.
        """
        closing_price_df = self.Stock_historical_data_df
        
        log_returns = self.logarithmic_returns()
        drift = self.compute_drift()
        
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
            
            # self.plot_graph(price_list,stock)            

        
        return all_simulation
    
    
    def predict_daily_price_cholesky_decomposition(self,period,iterations):
        """
        Use Monte Carlo Simulation to predict the stock price.

        Parameters
        ----------
        period : int
            The time horizon in days for which to predict stock prices.
        iterations : int
            The number of simulations to run for each stock.

        Returns
        -------
        Dict[str, pd.DataFrame]
            A dictionary containing the simulation results for all the stocks provided.
            The keys of the dictionary are the stock names, and the values are pandas
            DataFrames containing the simulated prices.
        """
        closing_price_df = self.Stock_historical_data_df
        
        #Basic information and data
        log_returns = self.logarithmic_returns()
        temp_stock_list = list((log_returns.columns))
        numstocks = len(temp_stock_list)

        #Brownian motion component: drift
        drift = self.compute_drift()
        
        #Cholesky decomposition
        covari = log_returns.cov()        
                
        chol = np.linalg.cholesky(covari)        
        
        #Generate uncorralated random variables and use cholesky decomposition to correlate them
        uncorr_x = norm.ppf(np.random.rand(numstocks,iterations*period))
        
        corr_x = np.dot(chol, uncorr_x)

        #Calculate daily return
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
            
            # self.plot_graph(price_list,stock) 
            stock_index +=1
            # break
        # print(temp_df)
        
        return all_simulation
    
    

    def combine_the_predict_price(self,simulation_result):
        """
        Combine the prediction price data to make it as a DataFrame that we use to do historical simulation.

        Parameters
        ----------
        simulation_result : Dict[str, pd.DataFrame]
            A dictionary containing the simulation results for all the stocks provided.
            The keys of the dictionary are the stock names, and the values are pandas
            DataFrames containing the simulated prices.

        Returns
        -------
        Dict[str, pd.DataFrame]
            A dictionary containing all the simulations for the entire portfolio.
            The keys of the dictionary are the simulation days, and the values are pandas
            DataFrames containing the simulated prices for each stock.
        """        
        all_portfolio_prediction = {}
        
        stocks = list(simulation_result.keys())
        price_dfs = list(simulation_result.values())

        concat_df = None
        for single_day_prediction_index in range(len(price_dfs[0].columns)):
            
            for stock_index in range(len(stocks)):
                temp_df = price_dfs[stock_index][single_day_prediction_index].copy()
                
                
                if stock_index == 0:
                    concat_df = temp_df.to_frame()
                    concat_df.rename({single_day_prediction_index: f'{stocks[0]}'},axis=1, inplace=True)
                else:
                    concat_df[stocks[stock_index]] = temp_df
                    
                
            
                all_portfolio_prediction[f'prediction_{single_day_prediction_index}'] = concat_df  
            # break
        # concat_df.to_csv('concat_df.csv')
            
        return all_portfolio_prediction
    
    
    
    def using_HS_to_get_var(self,all_portfolio_prediction,Time,InitialInvestment,confidence_level):
        """
        Uses Historical Simulation to predict the VaR and CVaR for the given portfolio.

        Parameters
        ----------
        all_portfolio_prediction : dict
            A dictionary containing all the simulation for all the portfolios.
        Time : int
            Time horizon for the calculation.
        InitialInvestment : float
            Initial Investment for your portfolio or stock.
        confidence_level : float
            The confidence level for VaR or CVaR.

        Returns
        -------
        tuple
            A tuple of two floats containing the predicted VaR and CVaR for the given portfolio.
        """
        
        portfolio_weights = self.portfolio_weights
        
        hVaR_list = []
        hCVaR_list = []
        
        for predict_df in list(all_portfolio_prediction.values()):
            predict_df = predict_df.copy()
            
            portfolio_stock_object = Historical_Simulation(predict_df,portfolio_weights)
                        
            VaR = (portfolio_stock_object.Calculating_VaR_by_Historical_Simulation(confidence_level))

            CVaR = (portfolio_stock_object.Calculating_CVaR_by_Historical_Simulation(confidence_level))

            hVaR = portfolio_stock_object.quantile_to_VaR(VaR,Time,InitialInvestment)

            hCVaR = portfolio_stock_object.quantile_to_VaR(CVaR,Time,InitialInvestment)

            hVaR_list.append(hVaR)
            hCVaR_list.append(hCVaR)
            
            
        
        hVaR_list = np.array(hVaR_list)
        hCVaR_list = np.array(hCVaR_list)
        # print(hVaR_list)
        
        
        mc_var = np.percentile(hVaR_list,100-confidence_level)
        mc_Cvar = np.percentile(hCVaR_list,100-confidence_level)
        
        return (mc_var,mc_Cvar)
        
N = norm.cdf
class cal_option_price(data_initialise):
    """
    cal_option_price is a class that calculates the VaR for an option contract.

    Parameters
    ----------
    ticker : str
        The ticker symbol for the stock of the option contract.
    option_type : str
        The type of the option contract: "call" or "put".
    strike_price : float
        The strike price for the option contract.
    expiration_date : datetime
        The expiration date for the option contract.
    risk_free_rate : float
        The risk-free rate for the option contract.

    Methods
    -------
    cal_sigma(self) -> float:
        Calculates the annualized volatility of the underlying stock.
        
    cal_d1_d2(self,S:float, sigma:float, t:int) -> Tuple[float]:
        Calculates the d1 and d2 parameters of the Black-Scholes formula.
        
    black_scholes(self,S:float, sigma:float, t:int) -> float:
        Calculates the price of an option contract using the Black-Scholes formula.
    """
    
    def __init__(self, ticker, option_type, strike_price, expiration_date,risk_free_rate):
        self.ticker = ticker
        self.option_type = option_type
        self.strike_price = strike_price
        self.expiration_date = expiration_date
        self.risk_free_rate = risk_free_rate
    
        
    def cal_sigma(self):
        """
        Calculates the annualized volatility of the underlying stock.

        Returns
        -------
        float
            The annualized volatility of the underlying stock.
        """
        stock_list = [self.ticker]
        # data that take to calculated the 
        period = 501
        # print(f'period = {period}')
        
        portfolio_stock_data = Get_the_stock_data.Get_the_stock_portfolio_historical_data_in_the_given_time(stock_list,period)
        
        self.Stock_historical_data_df = portfolio_stock_data
        
        daily_returns = self.Calculating_daily_portfolio_Returns()
        # print(daily_returns)
        
        daily_std = daily_returns.std()
        annual_std = daily_std * np.sqrt(252)        
        
        return annual_std
    
    def cal_d1_d2(self,S,sigma,t):
        """
        Calculates the d1 and d2 parameters of the Black-Scholes formula.

        Parameters
        ----------
        S : float
            The current stock price.
        sigma : float
            The volatility of the stock.
        t : int
            The time (in days) until expiration.

        Returns
        -------
        Tuple[float]
            The values of d1 and d2.
        """
        
        X = self.strike_price
        r = self.risk_free_rate
        dt = (((self.expiration_date - pd.Timestamp.today()).days) - t )/365        
        
        d1 = ((np.log((S/X)))+((r+((sigma**2)/2))*(dt))) / (sigma * np.sqrt(dt))
        d2 = ((np.log((S/X)))+((r-((sigma**2)/2))*(dt))) / (sigma * np.sqrt(dt))
        
        return d1,d2

    
    def black_scholes(self,S,sigma,t):
        """
        Calculates the price of an option contract using the Black-Scholes formula.

        Parameters
        ----------
        S : float
            The current stock price.
        sigma : float
            The volatility of the stock.
        t : int
            The time (in days) until expiration.

        Returns
        -------
        float
            The price of the option contract.
        """
        option_type = self.option_type
        r = self.risk_free_rate
        X = self.strike_price
        dt = (((self.expiration_date - pd.Timestamp.today()).days) - t )/365        
        
        d1,d2 = self.cal_d1_d2(S,sigma,t)
        
        option_price = None
        if option_type == "call":
            option_price = (S*N(d1)) - (X*np.exp(-r*(dt)) * N(d2))
        elif option_type == "put":
            option_price = ((X*np.exp(-r*(dt))) * (N(-d2))) - (S*N(-d1))

        
        return option_price

class OptionVaR():
    """
    A class for calculating the Value at Risk (VaR) of a portfolio of options.

    Parameters
    ----------
    options_data : pd.DataFrame
        A DataFrame containing option data, including stock tickers, option types,
        strike prices, expiration dates, risk-free rates, portfolio weights, and
        number of options.
    confidence_level : float
        The confidence level for calculating VaR.
    simulated_stock_prices : Optional[dict]
        A dictionary containing simulated stock prices for each stock ticker.

    Attributes
    ----------
    options_data : pd.DataFrame
        A DataFrame containing option data.
    simulated_stock_prices : Optional[dict]
        A dictionary containing simulated stock prices for each stock ticker.
    confidence_level : float
        The confidence level for calculating VaR.
    
    Methods
    -------
    calculate_var() -> float:
        Calculates VaR using historical stock prices.
    calculate_var_monte_carlo() -> float:
        Calculates VaR using Monte Carlo simulation.
    """
    def __init__(self, options_data, confidence_level, simulated_stock_prices=None):
        self.options_data = options_data
        self.simulated_stock_prices = simulated_stock_prices
        self.confidence_level = confidence_level
                
    def calculate_var(self):
        """
        Calculates VaR using historical stock prices.

        Returns
        -------
        float
            The VaR of the portfolio.
        """
        all_option_price_returns = []

        for index, ticker in enumerate(self.options_data['stock_list']):
        
            option_data_with_rf = {
                "ticker": ticker,
                "option_type": self.options_data['option_type'][index],
                "strike_price": self.options_data['strike_price'][index],
                "expiration_date": pd.Timestamp(self.options_data['expiration_date'][index]),
                "risk_free_rate": self.options_data['risk_free_rate']
            }
            option = cal_option_price(**option_data_with_rf)
            weight = self.options_data['portfolio_weights'][index]
            num_options = self.options_data['number_of_options'][index]
            sigma = option.cal_sigma()[option.ticker]
            day_to_maturity = (option.expiration_date - pd.Timestamp.today()).days
            temp_df = option.Stock_historical_data_df.tail(day_to_maturity).copy()
            # print(temp_df)

            option_prices = []

            for i in range(0, day_to_maturity-1):
                S = temp_df[option.ticker].iloc[i]
                option_price = (option.black_scholes(S, sigma, i))
                option_prices.append(option_price)

            option_price_returns = [(option_prices[i+1] - option_prices[i]) * weight * num_options for i in range(len(option_prices) - 1)]
            all_option_price_returns.extend(option_price_returns)

        portfolio_VaR = np.percentile(all_option_price_returns, 100 - self.options_data['confidence_level'])

        # print(f"Value at Risk 95th CI    :       {portfolio_VaR}")

        return portfolio_VaR
    
    def calculate_var_monte_carlo(self):
        """
        Calculates VaR using Monte Carlo simulation.

        Returns
        -------
        float
            The VaR of the portfolio.
        """
        
        if self.simulated_stock_prices is None:
            raise ValueError("Simulated stock prices not provided.")
        
        all_option_price_returns = []

        for index, ticker in enumerate(self.options_data['stock_list']):
            option_data_with_rf = {
                "ticker": ticker,
                "option_type": self.options_data['option_type'][index],
                "strike_price": self.options_data['strike_price'][index],
                "expiration_date": pd.Timestamp(self.options_data['expiration_date'][index]),
                "risk_free_rate": self.options_data['risk_free_rate']
            }
            option = cal_option_price(**option_data_with_rf)
            weight = self.options_data['portfolio_weights'][index]
            num_options = self.options_data['number_of_options'][index]
            sigma = option.cal_sigma()[option.ticker]
            day_to_maturity = (option.expiration_date - pd.Timestamp.today()).days
            
            # Use simulated stock prices from simulated_stock_prices attribute
            simulated_stock_prices = self.simulated_stock_prices[ticker].tail(day_to_maturity).copy()
            option_prices = []

            for i in range(0, day_to_maturity-1):
                S = simulated_stock_prices.iloc[i]
                option_price = (option.black_scholes(S, sigma, i))
                option_prices.append(option_price)

            option_price_returns = [(option_prices[i+1] - option_prices[i]) * weight * num_options for i in range(len(option_prices) - 1)]
            all_option_price_returns.extend(option_price_returns)


        portfolio_VaR = np.percentile(all_option_price_returns, 100 - self.options_data['confidence_level'])

        # print(f"Value at Risk 95th CI    :       {portfolio_VaR}")

        return portfolio_VaR

