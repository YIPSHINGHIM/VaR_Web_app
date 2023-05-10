from django.urls import path

from . import views

urlpatterns = [
    path('get_data_view', views.get_data_view, name="received user input"),
    path('graph_data',views.graph_data,name="send graph data"),
    path('simulation', views.simulation, name="simulation endpoint"),
    path('option_data',views.option_data,name="received option Data"),
    path('option_var',views.option_var,name="option_var"),

]

