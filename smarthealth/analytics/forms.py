from django import forms


class CEForm(forms.Form):
    NOYES = (
        (0, 'No'), (1, 'Yes')
    )

    gender = forms.ChoiceField(choices=(('male', 'male'), ('female', 'female')))
    race = forms.CharField()
    postal_code = forms.IntegerField()
    occupation = forms.CharField()
    weight = forms.IntegerField()
    bp_hosp_min = forms.IntegerField()
    bp_hosp_max = forms.IntegerField()

    diabetes = forms.ChoiceField(choices=NOYES)
    hiv = forms.ChoiceField(choices=NOYES)
    cancer = forms.ChoiceField(choices=NOYES)

    dexamethasone = forms.ChoiceField(choices=NOYES)
    erlotinib = forms.ChoiceField(choices=NOYES)

    bp_disch_min = forms.IntegerField()
    bp_disch_max = forms.IntegerField()
