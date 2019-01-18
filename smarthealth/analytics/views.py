import os
import pdb

from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
from sklearn.linear_model import LogisticRegression

from . import models
from . import forms

d_procedures = {3000:'Carotid endarterectomy'}
d_diagnoses = {10000:'diabetes', 10001:'hiv', 10002:'cancer'}
d_chartevents = {2000:'weight', 2001:'abp'}


def transform_categorical(df):
    """
    Transform all the categorical variables in the dataframe
    """
    categoricals = []

    for feature in ['gender', 'race', 'postal_code', 'occupation']:
        categoricals.append(pd.get_dummies(df[feature], prefix=feature))
        del(df[feature])

    df = pd.concat([df] + categoricals, axis=1)
    return df


def analyze_new_patient(request):
    """
    Page to input data about a patient and model the likeliness
    of readmission after carotid endartorectomy

    """

    if request.method == 'POST':
        form = forms.CEForm(data=request.POST)

        if form.is_valid():
            # Put it in the form that the machine learning model expects
            df = pd.DataFrame({
                'gender':[form.cleaned_data['gender']],
                'race':[form.cleaned_data['race']],
                'postal_code':[int(form.cleaned_data['postal_code'])],
                'occupation':[form.cleaned_data['occupation']],
                'weight':[int(form.cleaned_data['weight'])],
                'bp_hosp_min':[int(form.cleaned_data['bp_hosp_min'])],
                'bp_hosp_max':[int(form.cleaned_data['bp_hosp_max'])],
                'diabetes':[int(form.cleaned_data['diabetes'])],
                'hiv':[int(form.cleaned_data['hiv'])],
                'cancer':[int(form.cleaned_data['cancer'])],
                'dexamethasone':[int(form.cleaned_data['dexamethasone'])],
                'erlotinib':[int(form.cleaned_data['erlotinib'])],
                'bp_disch_min':[int(form.cleaned_data['bp_disch_min'])],
                'bp_disch_max':[int(form.cleaned_data['bp_disch_max'])],
                # Dummy data for now
                'readmission':[0],
            })


            # Read the prepared training data
            df_train = pd.read_csv(os.path.join(settings.BASE_DIR, '..',
                'data', 'study-table.csv'))
            # Preprocess data
            df = pd.concat([df_train, df])
            df = transform_categorical(df)


            # Train the machine learning model on previous cases
            x_train = df.iloc[:-1, :-1]
            y_train = df.iloc[:-1, -1]

            x_test = df.iloc[-1, :-1].reshape(1, -1)

            # Use the ML model to predict this patient's outcome
            clf_lr = LogisticRegression()
            clf_lr.fit(x_train, y_train)

            prediction = clf_lr.predict(x_test)[0]
        # No analysis done if data not input correctly
        else:
            prediction = -1
    else:
        # No analysis done
        form = forms.CEForm()
        prediction = -1

    return render(request, 'analytics/analyze_new_patient.html', {
        'form':form, 'prediction':prediction})


def analyze_patient(request, patient_id):
    """
    Analyze a patient's likeliness of being readmitted after
    carotid endartorectomy
    """

    # Get the patient's data
    patient = Patient.objects.get(patient_id=patient_id)

    # Check for hospital admission with caro endar
    admissions = Patient.admissions.all()

    procedure = patient.admissions.filter(hadm_id__in=[a.hadm_id for a in admissions])

    # Patient had the procedure
    if procedure:
        # This is the admission with the procedure
        admission = procedure.get()
        weight = admission.chartevents.get(item_id=2000)

        # Get the max and min blood pressures from the hospital admission
        hospital_bps = admission.chartevents.filter(item_id=2001)
        bp_hosp_min = min(b.value for b in hospital_bps)
        bp_hosp_max = max(b.value for b in hospital_bps)

        # Get the comorbidities
        diabetes = bool(admission.diagnoses.filter(icd9_code=10000))
        hiv = bool(admission.diagnoses.filter(icd9_code=10001))
        cancer = bool(admission.diagnoses.filter(icd9_code=10002))

        # Get the medications
        dexamethasone = bool(patient.medications.filter(drug='dexamethasone'))
        erlotinib = bool(patient.medications.filter(drug='erlotinib'))

        # Get the bp stream values
        bp_disch = patient.bpstream.filter(datetime__gt=admission.outtime)

        bp_disch_min = min(b.bp_min for b in bp_disch)
        bp_disch_max = max(b.bp_max for b in bp_disch)

        # Put it in the form that the machine learning model expects
        df = pd.DataFrame({
            'gender':[patient.gender], 'race':[patient.race],
            'postal_code':[patient.postal_code],
            'occupation':[patient.occupation],
            'weight':[weight],
            'bp_hosp_min':[bp_hosp_min],
            'bp_hosp_max':[bp_hosp_max],
            'diabetes':[diabetes],
            'hiv':[hiv], 'cancer':[cancer],
            'dexamethasone':[dexamethasone],
            'erlotinib':[erlotinib],
            'bp_disch_min':[bp_disch_min],
            'bp_disch_max':[bp_disch_max]})

        df = transform_categorical(df)

        # Train the machine learning model on previous cases
        x_train = pd.read_csv(os.path.join(settings.BASE_DIR, '..',
            'data', 'study-table.csv'))
        y_train = df['readmission'].values
        x_train = x_train.iloc[:, :-1]
        x_train = transform_categorical(x_train)

        clf_lr = LogisticRegression()
        clf_lr.fit(x_train, y_train)

        # Use the ML model to predict this patient's outcome
        y_predict_lr = clf_lr.predict(x_test)[0]

        context = {'valid':True,

            'predicted_outcome':y_predict_lr}
    # Patient did not have the procedure
    else:
        context = {'valid':False}


    return render(request, 'analtics/analyze_patient.html', context=context)
