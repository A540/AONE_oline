"""Aone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from .views import UploadLog, DeleteLogView, get_logs_by_month, Get_log

urlpatterns = [
    path('upload', UploadLog.as_view()),
    path('delete_log/<int:log_id>/', DeleteLogView.as_view(), name='delete_log'),
    path('check/<str:year_month>/', get_logs_by_month, name='get_logs_by_month'),
    path('get-log-by-id/', Get_log.as_view()),
]
