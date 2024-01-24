from django.urls import path
from . import views

urlpatterns = [
    path('', views.DataList, name='DataList'),
    path('latest/', views.Latest, name='DataList'),
]