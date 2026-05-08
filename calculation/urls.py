from django.urls import path
from . import views

urlpatterns = [
    path('submit-final/', views.submit_final_application, name='submit_final'),
]