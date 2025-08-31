

# Register your models here.
from django.contrib import admin
from .models import Prediction

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'area_sqft', 'predicted_price', 'predicted_at')
