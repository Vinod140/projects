A Django-based web application that predicts property prices based only on area (sq. ft.) using a machine learning model built with Scikit-learn. The app provides a simple web interface where users can input the area of land/house and instantly get an estimated price.

🚀 Features

Django Web Application – Fully functional backend with HTML/CSS frontend.

Price Prediction – Predicts property price solely based on area (sq. ft.).

Machine Learning Model – Built using Scikit-learn regression.

Interactive UI – Simple input form and clean results page.

Instant Results – Real-time predictions without delay.

🛠️ Tech Stack

Backend: Django (Python)

Frontend: HTML, CSS

Machine Learning: Scikit-learn (Linear Regression or similar)

Other Libraries: Pandas, NumPy (for preprocessing)

⚙️ Workflow

Dataset Preparation

Dataset contains Area (sq. ft.) and corresponding Price.

Clean and preprocess data using Pandas & NumPy.

Model Training

Train regression model (e.g., Linear Regression) with Area → Price.

Save trained model as model.pkl.

Django Integration

User enters area in a web form.

Django backend loads the trained ML model.

Model predicts the price for the given area.

Predicted price is displayed on results page.
