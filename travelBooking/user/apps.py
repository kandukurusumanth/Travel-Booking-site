from django.apps import AppConfig

class UserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'travelBooking.user'       
    label = 'travelbooking_user'

    def ready(self):
        import travelBooking.user.signals
