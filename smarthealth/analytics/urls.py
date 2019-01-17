from django.urls import path

from . import views


urlpatterns = [
    path('analyze-patient/<patient_id>/', views.analyze_patient)

]
