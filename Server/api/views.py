import uuid

from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Data_for_Option_VaR, Data_for_VaR
from .VaR_app.Calculating_VaR_folder.app import *

# Create your views here.

@api_view(['POST'])
def get_data_view(request):
    try:
        data = (request.data).dict() 
        
    except:
        print(request.data)
        # print(type(request.data))
        data = (request.data)
    print(data)
    # check_flag , respond = check_user_input(data)
    check_flag , respond = check_Stock_user_input(data)

    
    if check_flag:
        
        data_id = uuid.uuid1()
        
        new_data = Data_for_VaR.objects.create(
            Data_id = str(data_id),
            period = int(data['period']),
            Time = int(data['Time']),    
            InitialInvestment = float(data['InitialInvestment']),
            stock_list = data['stock_list'],
            portfolio_weights_str = data['portfolio_weights'],
            confidence_level = data['confidence_level']
        )
        new_data.save()
        print(data_id)
    
    return Response(check_flag)


@api_view(['GET','POST'])
def option_data(request):
    try:
        data = request.data.dict()
    except:
        data = request.data
    print(data)
    check_flag , respond = check_Option_user_input(data)
    
    if check_flag:
        return Response(True)
    else:
        return Response(False)


@api_view(['GET','POST'])
def option_var(request):
    try:
        data = request.data.dict()
    except:
        data = request.data
    print(data)
    # print(type(data['method']))
    method = data['method']
    

    check_flag , respond = check_Option_user_input(data)
        
    if check_flag:
        clean_option_data = make_clean_option_data(data)            

        if method == "hs":    
            option_var = option_HS_var(clean_option_data)
            
        elif method == "ms":
            option_var = option_MS_var(clean_option_data)
        else:
            return Response (False)

        print(option_var)        
        return Response(option_var)
    else:
        return Response(False)
    

    


@api_view(["GET","POST"])
def graph_data(request):
    
    try:
        data = request.data.dict()
    except:
        data = request.data
    print(data)

    latest_data = Data_for_VaR.objects.latest('created_at')
    clean_data = make_clean_data(latest_data)

    portfolio_stock_data, portfolio_returns = pd_to_json(clean_data)

    
    if data['type'] == "ClosingPrice":
        return Response(portfolio_stock_data)
    elif data['type'] == "Return":
        return Response(portfolio_returns)
    else:
        raise ValidationError("Invalid request: type parameter must be 'ClosingPrice' or 'Return'")
    

@api_view(['GET',"POST"])
def simulation(request):
    latest_data = Data_for_VaR.objects.latest('created_at')
    # print(latest_data)
    # print(latest_data.Data_id)
    clean_data = make_clean_data(latest_data)
    # print(clean_data)
  
    try : 
        data = (request.data).dict() 
    except:
        data = request.data
    print(data)
    
    method = str(data["method"])
    
    if method == "hs":
        return_data = historical_simulation_portfolio(clean_data)

        print("1################################################")
        print(return_data)
        
        del clean_data 
        del latest_data 
        
        return Response(return_data)
    if method == "mb_1":  
        return_data = parametric_method_one_portfolio(clean_data)
        print("2################################################")
        print(return_data)
        
        del clean_data 
        del latest_data 
        
        return Response(return_data)
    if method == "mb_2":  
        hVaR = parametric_method_two_portfolio(clean_data)
        # print(hVaR)
        
        del clean_data 
        del latest_data 
        
        return Response(hVaR)
    if method == "ms_1":  
        return_data = Monte_Carlo_Simulation_method_one_portfolio(clean_data)
        print("3################################################")
        print(return_data)
        
        del clean_data 
        del latest_data 
        
        return Response(return_data)
    if method == "ms_2":  
        hVaR = Monte_Carlo_Simulation_method_two_portfolio(clean_data)
        # print(hVaR)
        
        del clean_data 
        del latest_data 
        return Response(hVaR)
        
    return Response("Error no method provided ")

