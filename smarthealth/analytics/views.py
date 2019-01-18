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
