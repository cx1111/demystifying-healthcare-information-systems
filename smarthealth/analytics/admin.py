from django.contrib import admin

from . import models


patients = ['patient_id', 'dob', 'gender', 'race', 'postal_code', 'occupation']
admissions = ['patient_id', 'hadm_id', 'intime', 'outtime']
procedures = ['hadm_id', 'icd9_code']
diagnoses = ['hadm_id', 'icd9_code']
chartevents = ['hadm_id', 'item_id', 'value', 'datetime']
bpstream = ['patient_id', 'datetime', 'bp_min', 'bp_max']
medications = ['patient_id', 'datetime', 'drug']


admin.site.register(models.Patient)
admin.site.register(models.Admission)
admin.site.register(models.Procedure)
admin.site.register(models.Diagnosis)
admin.site.register(models.Chartevent)
admin.site.register(models.BloodPressureStream)
admin.site.register(models.Medication)
