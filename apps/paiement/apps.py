from django.apps import AppConfig
import joblib
import os

class PaiementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.paiement'
    
    def ready(self):
        model_path = os.path.join(self.path, 'model.pkl')
        self.model = joblib.load(model_path)
