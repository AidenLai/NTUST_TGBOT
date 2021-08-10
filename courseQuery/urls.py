from django.urls import path

from courseQuery import views

urlpatterns = [
    path('', views.webhook_handler)
]
