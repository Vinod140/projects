from django.db import models

class Prediction(models.Model):
    full_name = models.CharField(max_length=100)
    address = models.TextField()
    mobile = models.CharField(max_length=15)
    age = models.IntegerField()
    area_sqft = models.FloatField()
    predicted_price = models.FloatField()
    predicted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - ₹{self.predicted_price} Lakh"
