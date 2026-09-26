from django.urls import path
from .views import  LifeLongCreateView

urlpatterns = [
    path('life-long/create', LifeLongCreateView.as_view(), name='life-long-create'),
]