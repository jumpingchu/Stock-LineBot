from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from stock_public_api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url('callback', views.callback)
]
