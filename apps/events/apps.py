from django.apps import AppConfig
import joblib
import os
import pandas as pd

class EventsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.events'

    model_path = os.path.join(os.path.dirname(__file__), 'random_forest_price_predictor.pkl')
    price_predictor_model = joblib.load(model_path)
