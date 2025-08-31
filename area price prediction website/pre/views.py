from django.shortcuts import render
from .forms import AreaForm
from .models import Prediction
import os
from joblib import load

# Load the ML model
model_path = os.path.join(os.path.dirname(__file__), 'model', 'area_price_pred.pkl')
model = load(model_path)

def predict_price(request):
    predicted_price = None
    user_data = {}

    form = AreaForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        area = form.cleaned_data['area_sqft']
        prediction = model.predict([[area]])
        predicted_price = round(prediction[0], 2)

        # Save to database
        Prediction.objects.create(
            full_name=form.cleaned_data['full_name'],
            address=form.cleaned_data['address'],
            mobile=form.cleaned_data['mobile'],
            age=form.cleaned_data['age'],
            area_sqft=area,
            predicted_price=predicted_price
        )

        user_data = {
            'full_name': form.cleaned_data['full_name'],
            'address': form.cleaned_data['address'],
            'mobile': form.cleaned_data['mobile'],
            'age': form.cleaned_data['age'],
        }

    return render(request, 'predict_form.html', {
        'form': form,
        'predicted_price': predicted_price,
        'user_data': user_data
    })
