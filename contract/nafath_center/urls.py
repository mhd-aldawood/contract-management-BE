from django.urls import path
from .views import NafathCenterCreateView, NafathCenterListView

urlpatterns = [
    path('nafath-center/create', NafathCenterCreateView.as_view(), name='nafath-create'),
    path('nafath-center/',        NafathCenterListView.as_view(),   name='nafath-list'),
]