
# Term 1
## 03-10-2022
- First meeting with project supervisor talk about the project plan and suggest reading 

## 04-10-2022
- Initialise the project repo and do the first commit 

## 08-10-2022
- Today I try to calculate the returns using the historical data , also try to calculate their Mean, variance, and normal distribution,

- Try to get a stock Portfolio data 

## 09-10-2022
- understanding of investing by constructing portfolios of assets to enhance your risk-adjusted returns. And try to implement it using python

## 14-10-2022
- Try to implement Factor Investing , and learn about the main factors that influence the returns of your portfolios and how to quantify your portfolio's exposure to these factors.

## 15-10-2022 
- try to implement the formula using python and try to understand how value at risk work

## 21-10-2022
- create a function to get the time frame 
- create a function to get the single stock data
- create a function to calculate the daily stock return

## 22-10-2022
- try to use TDD method to develop my app

## 24-10-2022 
- make a function to create a stock object
- refactor the Get_the_single_stock_historical_data_in_the_given_time function 

## 27-10-2022
- make a function Calculating daily stock Returns 
- refactor the code to become a better python application layouts

## 28-10-2022
- try get the stock data as a portfolio
- try to make a function to calculate the VaR by giving it a portfolio data 

## 3-11-2022
- updated the test_Calculating_daily_stock_Returns function , now it can calculate the return in a period of time 

## 4-11-2022
- update the function in Calculate_VaR.py combine the Calculating_VaR_by_Historical_Simulation function to a single function , now it can accept single stock or a portfolio

## 5-11-2022
- refactor the code , restructure the Calculate_VaR class , now I have a sub class call Historical_Simulation for Historical Simulation to calculate the VaR and CVaR

## 12-11-2022
- refactor the code , now all function separate to different class 
- try to make the Calculating_VaR_by_parametric_method function

## 13-11-2022
- added some new test case for Calculating_VaR_by_Historical_Simulation function
- implement the Calculating_VaR_by_parametric_method function

## 20-11-2022 
- learn how to make the Monte Carlo Simulation 

## 26-11-2022
- updated the test case
- move the driver code to main.py

## 27-11-2022
- create the function for Calculating portfolio VaR by parametric method 

## 29-11-2022
- fixing bugs for Calculating_VaR_by_parametric_method_portfolio 

## 30-11-2022
- make back test for using historical simulation for single stock and portfolio

## 1-12-2022
- created a function to calculated VaR or CVaR by giving it quantile time horizon and InitialInvestment 

# Term 2
## 6-1-2023
- upgrade the programs to API 

## 7-1-2023
- try to understand the Monte Carlo Simulation
- research on Brownian motion
- research on drift 
- research on Cholesky decomposition 

## 8-1-2023
- implemented logarithmic_returns function to calculate the log return 
- implemented the compute_drift function to calculated the drift 
- implemented the predict_daily_price function , which use Monte Carlo Simulation to predicted the stock price and return it as a dictionary 

## 9-1-2023
- implemented the combine_the_predict_price function to combine the data in the dictionary into a dataframe for pass in to other function to calculated the VaR 
- implemented the using_HS_to_get_var function to calculated the VaR by the given dataframe the generated from combine_the_predict_price function

## 10-1-2023
- implemented the predict_daily_price_cholesky_decomposition function , this simulation is using cholesky decomposition 
- added the test case for the function 

## 13-1-2023
- looking in to the Derivatives

## 15-1-2023 
- had meeting with professor , get feedback from him 

## 17-1-2023 
- updated the report , changes the formula in the report and updated some of the style 

## 18-1-2023
- added the back test for historical simulation @ portfolio
- move it to the testing file 

## 20-1-2023
- added the back test for parametric method @single stock method 1 
- added the back test for parametric method @portfolio method 1

## 22-1-2023
- added the back test for parametric method @single stock method 2
- added the back test for parametric method @portfolio method 2

## 26-1-2023 
- fixed the importing bugs with django 
- restructure the code , moved the quantile_to_VaR function to data_initialise class 


## 1-2-2023 
- added the driver code for Monte Carlo simulation @ single stock method 1
- added the driver code for Monte Carlo simulation @ single stock method 2
- added the back test for Monte Carlo simulation @single stock method 1
- added the back test for Monte Carlo simulation @portfolio method 1
- added the back test for Monte Carlo simulation @single stock method 2
- added the back test for Monte Carlo simulation @portfolio method 2

## 12-2-2023 
- added a check_stock_exists function to check the given stock list from user 
- added a check_weight function to check the given stock list from user 
- added test case for check_stock_exists and check_weight function

## 13-2-2023
- updated the function in app.py , now it can accept user input 
- upgrade the software to api , now user can do the simulation by call the api 
- refactor the code in app.py (remove the dead code)

## 20-2-2023
- refactor the code in app.py 

## 21-2-2023
- start the frontend , by using react 
- create 3 pages using react router dom 

## 22-2-2023 
- created the navBar and SideBar 
- created the Form components to accept user input 

## 27-2-2023 
- made the function to fetch API  , now user can fetch the api by given params

## 28-2-2023
- added a new field in to database to store the creation date
- added a graph component in frontend , now it can display the closing price 

## 3-3-2023 
- Update the sideBar component 
- created new page in project (calculated VaR in different method and VaR with option price)

## 4-3-2023 
- create a graph for showcase the closing price 
- create a graph for showcase the return 

## 6-3-2023
- added the selection box , so the user can have different to calculated the VaR 
- start to implement the VaR for option price 

## 8-3-2023 
- implement component for render the VaR for single stock 

## 17-3-2023
- implement component for render the VaR for multiple stock  

## 20-3-2023
- start working on the Option VaR 
- create a class call cal_option_price for calculating the Option price 

## 21-3-2023 
- implement the Black-Scholes formula to calculated the Option price 
- made the cal_sigma, cal_d1_d2, black_scholes function 

## 22-3-2023
- implement the Option VaR 
- create a class call OptionVaR for calculating the value at risk for Option

## 24-3-2023 
- try to integrate the historical simulation with the Option VaR 
- try to integrate the Monte Carlo Simulation with the Option VaR 

## 25-3-2023
- covert the function to an api

## 26-3-2023 
- start marking the interface for the OptionVaR 
- made the OptionSideBar component 

## 28-3-2023
- integrate the OptionVaR api with the frontend 

## 29-3-2023
- refactor the code

