# User Manual

---

## Introduction
This user manual will guide you through using the Value-at-Risk (VaR) Web App and API to perform various financial calculations and retrieve historical stock data.

## Table of Content
* [Introduction](#introduction)
* [Installation](#installation)
* [API Usage](#api-usage)
* [Web App Usage](#web-app-usage)
  * [Getting Started](#getting-started)
  * [Navigating the Application](#navigating-the-application)
    * [Home Page](#home-page)
    * [VarDifferentMethod Page](#vardifferentmethod-page)
    * [VaRWithOption Page](#varwithoption-page)
  * [Additional Tips and Troubleshooting](#additional-tips-and-troubleshooting)


## Installation
---
### !!!　before you start make sure you have pip, python, npm and node install in your computer
First step make a new folder
```bash
mkdir value_at_risk
```

then go inside the value_at_risk folder
```bash
cd value_at_risk
```

then clone the repository , by using
```bash
git clone https://gitlab.cim.rhul.ac.uk/wjis203/PROJECT.git
```

---

## !!!! if you want to install by step by step you can ignore this cell , otherwise you can install by
go inside the repository
```bash
cd PROJECT
```

then run install.sh
``` bash
sh install.sh
```

to turn on the server
``` bash
sh start_server.sh
```

---

### continue for the installation
Because we want to make make the repository as clean as possible we decided to create the virtual environments out side the repository
```bash
python -m venv venv
```
After we created the virtual environments , we need to activated it <br>

#### for linux and mac user
```bash
. venv/bin/activate
```

#### for windows user
```bash
. venv/Scripts/activate
```

After we activated the environment we can go inside the repository
```bash
cd PROJECT
```

then update the pip and install the package
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

After that we need to go inside the server folder
```bash
cd Server
```

After we install the Django package, we need to do the migration to create the database for the server
```bash
python manage.py makemigrations api && python manage.py makemigrations && python manage.py migrate
```

if you want to create a admin account you need to use "createsuperuser" and follow the instruction
```bash
python manage.py createsuperuser
```

After we setup the backend , we need to setup the frontend , so we go in to the frontend folder
```bash
cd frontend
```

then we install the package for the frontend 
```bash
npm i
```

then we build the frontend , otherwise django cannot handle it 
```bash
npm run build
```

After all the data and user was created we can start the server now , by using

```bash
python manage.py runserver 5000
```

then the server will run on local host port 3000

## API Usage
---
Please read the API document

## Web App Usage
---
### Introduction
This user manual provides detailed instructions on how to use the Financial Risk Assessment Web Application. By following the steps outlined in this manual, users will be able to navigate the application, input data, choose calculation methods, and analyze the results of Value at Risk (VaR) and Option VaR calculations.

### Getting Started

#### Before start make sure you turn on the django server. 
To access the Financial Risk Assessment Web Application, open your preferred web browser and navigate to the [application's URL](http://localhost:5000/) (example:http://localhost:5000/).
! 
### Navigating the Application
Upon entering the application, users will be presented with three main pages: Home Page, VarDifferentMethod Page, and VaRWithOption Page. Use the Navbar located at the top of the application to switch between these pages.

#### Home Page
![](Document/images/Home%20page%20without%20data.png)
The Home Page displays 2 graphs, which include the returns and closing price charts, and a sidebar for user input related to stock VaR calculations.
Enter the following input:
- stock_list: AAPL,MSFT
- portfolio_weights: 0.5,0.5
- period: 501
- Time Horizon: 1
- Initial Investment: 10000
- confidence_level: 5
Then, press the Submit button.
After submission, the application will display the graphs with the calculated data:

![](Document/images/Home%20page%20with%20data.png)

#### VarDifferentMethod Page
![](Document/images/Var%20Different%20Method%20without%20data.png)
When the user goes to the VarDifferentMethod page, the application will automatically calculate the VaR based on the input provided on the Home page.
The VarDifferentMethod Page also includes a sidebar for users to update their input provided on the Home page.
To update the input, enter all the data again into the input boxes:

- stock_list: AAPL,MSFT
- portfolio_weights: 0.5,0.5
- period: 501
- Time Horizon: 1
- Initial Investment: 10000
- confidence_level: 5

![](Document/images/Var%20Different%20Method%20with%20data.png)

The application will then display the VaR and CVaR calculated by different methods.
To calculate VaR using different methods, such as Historical Simulation and Monte Carlo Simulation, follow these steps:

![](Document/images/Var%20Different%20Method%20show%20method%20selection.png)

1. Choose the desired VaR calculation methods by selecting the appropriate checkboxes.
2. The application will update the results accordingly.

![](Document/images/Var%20Different%20Method%20show%20selected%20method%202.png)

#### VaRWithOption Page
![](Document/images/OptionVaR%20page%20with%20data.png)

The VaRWithOption Page has a different sidebar for user input and presents the results for calculating Option VaR using different methods.
To calculate Option VaR on the VaRWithOption Page, follow these steps:
In the OptionVaRSideBar, enter the required information:
- confidence_level: 5
- expiration_date: 2023-12-12,2023-12-24
- number_of_options: 10,10
- option_type: call,put
- portfolio_weights: 0.5,0.5
- risk_free_rate: 0.05
- stock_list: AAPL,MSFT
- strike_price: 150,120
The application will then display the Option VaR results.
Like this:
![](Document/images/OptionVaR%20page%20with%20data.png)

### Additional Tips and Troubleshooting
To ensure an optimal user experience, consider the following tips and troubleshooting steps:
- If the application is not displaying the expected results or is taking too long to load, refresh the web page and enter the input again.
- Make sure to input accurate and complete information in the StockVaRSideBar and OptionVaRSideBar components. Incorrect or incomplete data may lead to inaccurate results or errors.




