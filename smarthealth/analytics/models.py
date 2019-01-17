from django.db import models


# Recall the research tables
patients = ['patient_id', 'dob', 'gender', 'race', 'postal_code', 'occupation']
admissions = ['patient_id', 'hadm_id', 'intime', 'outtime']
procedures = ['hadm_id', 'icd9_code']
diagnoses = ['hadm_id', 'icd9_code']
chartevents = ['hadm_id', 'item_id', 'value', 'datetime']
bpstream = ['patient_id', 'datetime', 'bp_min', 'bp_max']
medications = ['patient_id', 'datetime', 'drug']


class Patient(models.Model):
    patient_id = models.IntegerField(primary_key=True)
    dob = models.DateTimeField()
    gender = models.CharField(max_length=20)
    race = models.CharField(max_length=20)
    postal_code = models.IntegerField()
    occupation = models.CharField(max_length=20)


class Admission(models.Model):
    hadm_id = models.IntegerField(primary_key=True)
    patient = models.ForeignKey('analytics.Admission', related_name='admissions',
        on_delete=models.CASCADE)
    intime = models.DateTimeField()
    outtime = models.DateTimeField()


class Procedure(models.Model):
    admission = models.ForeignKey('analytics.Admission', related_name='procedures',
        on_delete=models.CASCADE)
    icd9_code = models.IntegerField()


class Diagnosis(models.Model):
    admission = models.ForeignKey('analytics.Admission', related_name='diagnoses',
        on_delete=models.CASCADE)
    icd9_code = models.IntegerField()


class Chartevent(models.Model):
    admission = models.ForeignKey('analytics.Admission', related_name='chartevents',
        on_delete=models.CASCADE)
    item_id = models.IntegerField()
    value = models.IntegerField()
    datetime = models.DateTimeField()


class BloodPressureStream(models.Model):
    patient = models.ForeignKey('analytics.Patient', related_name='bpstreams',
        on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    bp_min = models.IntegerField()
    bp_max = models.IntegerField()


class Medication(models.Model):
    patient = models.ForeignKey('analytics.Patient', related_name='medications',
        on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    drug = models.CharField(max_length=100)
