from django.urls import path

from userpart.models import MyConsumer

urlpatterns = [
    path('asyncpath/', MyConsumer.as_asgi())
]