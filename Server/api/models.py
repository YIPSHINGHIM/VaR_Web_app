import datetime

from django.db import models


# Create your models here.
class Data_for_VaR(models.Model):
    Data_id = models.CharField(max_length=36,primary_key=True)
    period = models.IntegerField()
    Time = models.IntegerField()
    InitialInvestment = models.FloatField()
    stock_list = models.CharField(max_length=500)
    portfolio_weights_str = models.CharField(max_length=500)
    confidence_level = models.FloatField()
    created_at = models.DateTimeField(default=datetime.datetime.now)
    
class Data_for_Option_VaR(models.Model):
    Data_id = models.CharField(max_length=36,primary_key=True)
    created_at = models.DateTimeField(default=datetime.datetime.now)
    stock_list = models.CharField(max_length=500)
    option_type_list = models.CharField(max_length=500)
    strike_price_list_str = models.CharField(max_length=500)
    expiration_date_list_str = models.CharField(max_length=500)
    portfolio_weights_str = models.CharField(max_length=500)
    risk_free_rate = models.FloatField()
    confidence_level = models.FloatField()
    number_of_options_list_str = models.CharField(max_length=500)

