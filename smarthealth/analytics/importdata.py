"""
Script for importing the research database content into django
"""
import datetime
import sqlite3

from django.utils.dateparse import parse_datetime
import pandas as pd

from analytics.models import Patient, Admission, Procedure, Diagnosis, Chartevent, BloodPressureStream, Medication

# Read the data from the research database
conn = sqlite3.connect('../data/allhealth.db')

df_patients = pd.read_sql_query('select * from patients;', conn)
df_admissions = pd.read_sql_query('select * from admissions;', conn)
df_procedures = pd.read_sql_query('select * from procedures;', conn)
df_diagnoses = pd.read_sql_query('select * from diagnoses;', conn)
df_chartevents = pd.read_sql_query('select * from chartevents;', conn)
df_bpstream = pd.read_sql_query('select * from bpstream;', conn)
df_medications = pd.read_sql_query('select * from medications;', conn)

conn.close()

patients = ['patient_id', 'dob', 'gender', 'race', 'postal_code', 'occupation']
admissions = ['patient_id', 'hadm_id', 'intime', 'outtime']
procedures = ['hadm_id', 'icd9_code']
diagnoses = ['hadm_id', 'icd9_code']
chartevents = ['hadm_id', 'item_id', 'value', 'datetime']
bpstream = ['patient_id', 'datetime', 'bp_min', 'bp_max']
medications = ['patient_id', 'datetime', 'drug']

for i in range(len(df_patients)):
    Patient.objects.create(
        patient_id=df_patients.loc[i, 'patient_id'],
        dob=parse_datetime(df_patients.loc[i, 'dob']),
        gender=df_patients.loc[i, 'gender'],
        race=df_patients.loc[i, 'race'],
        postal_code=df_patients.loc[i, 'postal_code'],
        occupation=df_patients.loc[i, 'occupation']
    )


x = datetime.datetime(1963, 1, 1, 1, 0)

