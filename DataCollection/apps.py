from django.apps import AppConfig
from . import worker

class DatacollectionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'DataCollection'