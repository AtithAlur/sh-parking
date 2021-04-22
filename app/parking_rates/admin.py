from django.contrib import admin
from .models import ParkingRate

# Register your models here.


class ParkingRateAdmin(admin.ModelAdmin):
    list_display = ['time_range', 'price']


admin.site.register(ParkingRate, ParkingRateAdmin)
