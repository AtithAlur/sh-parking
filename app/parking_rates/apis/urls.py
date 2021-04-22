from django.urls import path
from .views import RetrieveParkingPrice
from .admin.views import ListParkingRatesView, UpdateParkingRatesView

urlpatterns = [
    path('admin/rates', ListParkingRatesView.as_view()),
    path('admin/rates/update', UpdateParkingRatesView.as_view()),
    path('price', RetrieveParkingPrice.as_view())
]
