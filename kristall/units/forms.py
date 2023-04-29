from django import forms
# from django.forms.models import BaseInlineFormSet

from .models import Unit, Citys, Streets, Buildings, Flats, Image


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name', 'square']


class CitysForm(forms.ModelForm):
    class Meta:
        model = Citys
        fields = ['city']


class StreetsForm(forms.ModelForm):
    class Meta:
        models = Streets
        fields = ['street']


class BuildingsForm(forms.ModelForm):
    class Meta:
        models = Buildings
        fields = ['building', 'block', 'floors']


class FlatsForm(forms.ModelForm):
    class Meta:
        model = Flats
        fields = ['floor', 'flat']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
