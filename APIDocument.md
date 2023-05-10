# API document 
---
## Table of Content
* [get_data_view](#get_data_view)
* [graph_data](#graph_data)
* [simulation](#simulation)
* [option_data](#option_data)
* [option_var](#option_var)

---
## endpoint "get_data_view"
Endpoint: /get_data_view

Method: POST

Description: Receives user input for stock data and validates the data.

Request data:
JSON object containing the following data:
```json
{
  "stock_list": "AAPL,MSFT",
  "portfolio_weights": "0.5,0.5",
  "period": "501",
  "Time": "1",
  "InitialInvestment": "10000",
  "confidence_level": "5"
}

```
  
Response: A boolean value indicating if the user input is valid.

---
## endpoint "graph_data"

Endpoint: /graph_data

Method: POST

Description: Returns either the closing price data or return data for the portfolio stocks.

Request data:
type (string): The type of data requested, either "ClosingPrice" or "Return".
example : 
```json
{
	"type":"ClosingPrice"
}
```

Response: JSON object containing the requested data.
ClosingPrice respone: 
```json 
{
  "AAPL": {
    "2023-03-17 04:00:00": 155.0,
    "2023-03-20 04:00:00": 157.3999938965,
    ...
  },
  "TSLA": {
    "2023-03-17 04:00:00": 180.1300048828,
    "2023-03-20 04:00:00": 183.25,
    ...
  }
}

```

Return respone:
```json
{
  "AAPL": {
    "2023-03-17 04:00:00": -0.0054540011,
    "2023-03-20 04:00:00": 0.0154838316,
    ...
  },
  "TSLA": {
    "2023-03-17 04:00:00": -0.003440011,
    "2023-03-20 04:00:00": 0.0154356716,
    ...
  }
}
```
---
## endpoint "simulation"

Endpoint: /simulation

Method: POST

Description: Runs the selected VaR simulation method and returns the calculated VaR.

Request data:

method (string): The method to use for the simulation. Options: "hs", "mb_1", "mb_2", "ms_1", "ms_2".

| Method symbo | Method Name                        |
| ------------ | ---------------------------------- |
| hs           | historical Simulation              |
| mb_1         | Model Building Simulation method 1 |
| mb_2         | Model Building Simulation method 2 |
| ms_1         | Monte Carlo Simulation method 1    |
| ms_2         | Monte Carlo Simulation method 2    |

example : 
```json
{
	"method":"hs"
}
```


Response: JSON object containing the calculated VaR.
For method "mb_1", "mb_2" response is as follow :
```json
{
	"hVaR": 267.56053408332025,
	"InitialInvestment": 10000.0
}
```
For method "hs", "ms_1", "ms_2" response is as follow :
```json
{
	"hVaR": 267.56053408332025,
	"hVaR": 208.23633048603963,
	"InitialInvestment": 10000.0
}
```

---
## endpoint "option_data"

Endpoint: /option_data

Method: POST

Description: Receives and validates user input for option data.

Request data: JSON object containing the following data:

```json
{
  "confidence_level": "5",
  "expiration_date": "2023-12-12,2023-12-24",
  "number_of_options": "10,10",
  "option_type": "call,put",
  "portfolio_weights": "0.5,0.5",
  "risk_free_rate": "0.05",
  "stock_list": "AAPL,MSFT",
  "strike_price": "150,120"
}

```

Response: A boolean value indicating if the user input is valid.

---
## endpoint "option_var"

Endpoint: /option_var

Method: POST

Description: Calculates the Option VaR using the specified method (either "hs" or "ms").

Request data:

method (string): The method to use for the Option VaR calculation. Options: "hs", "ms".

| Method symbo | Method Name                        |
| ------------ | ---------------------------------- |
| hs           | historical Simulation              |
| ms           | Monte Carlo Simulation             |

example: 
```json
{
	"method":"hs"
}
```

Response: JSON object containing the calculated Option VaR.
```json
{
	"VaR": 267.56053408332025,
}
```