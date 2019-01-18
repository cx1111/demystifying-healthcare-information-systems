from django.urls import path

from . import views


urlpatterns = [
    path('analyze-patient/', views.analyze_new_patient,
        name='analyze_new_patient')
]
