from django import forms

from .models import HiddenGamePreferences


class DateSelectorForm(forms.Form):
    '''
    Form used for obtaining a date from the user.
    '''
    game_date = forms.DateField()


class HiddenGamePreferencesForm(forms.ModelForm):
    '''
    Form used for obtaining hidden score preferences from the user.
    '''
    class Meta:
        model = HiddenGamePreferences
        fields = ("hide_after_period", "max_score_difference")
