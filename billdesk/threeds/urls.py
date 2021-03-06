"""billdesk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('clone', views.clone, name='clone'),
    path('cleardb', views.cleardb, name='cleardb'),
    path('clearprepdb', views.clearprepdb, name='clearprepdb'),
    path('clearredis', views.clearredis, name='clearredis'),
    path('deployapp', views.deployapp, name='deployapp'),
    path('deploypreparatoryapp', views.deploypreparatoryapp, name='deploypreparatoryapp'),
    path('stopservicesthreedsapp', views.stopservicesthreedsapp, name='stopservicesthreedsapp'),
    path('stopservicespreparatorapp', views.stopservicespreparatorapp, name='stopservicespreparatorapp'),
    path('startservicesthreedsapp', views.startservicesthreedsapp, name='startservicesthreedsapp'),
    path('startservicespreparatorapp', views.startservicespreparatorapp, name='startservicespreparatorapp'),
    path('servicestatusthreedsapp',views.servicestatusthreedsapp, name='servicestatusthreedsapp'),
    path('servicesstatuspreparatorapp', views.servicesstatuspreparatorapp, name='servicesstatuspreparatorapp'),
    path('loadthreedsapp', views.loadthreedsapp, name='loadthreedsapp'),
    path('loadpreparatorapp', views.loadpreparatorapp, name='loadpreparatorapp'),
    path('refreshconfigapp', views.refreshconfigapp, name='refreshconfigapp'),
    path('refreshconfigpreparatorapp', views.refreshconfigpreparatorapp, name='refreshconfigpreparatorapp'),
    path('healthcheckapp', views.healthcheckapp, name='healthcheckapp'),
    path('healthcheckpreparatorapp', views.healthcheckpreparatorapp, name='healthcheckpreparatorapp'),
    path('updateconfig', views.updateconfig, name='updateconfig'),
    path('setdata', views.setdata, name='setdata'),
]
