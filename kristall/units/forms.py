from django import forms
from django.forms import modelformset_factory
from django.forms.models import BaseInlineFormSet

from .models import Image, Unit


class ElementInLineFormSet(BaseInlineFormSet):

    def clean(self):
        """Проверка заполнености полей."""
        super(ElementInLineFormSet, self).clean()
        if any(self.errors):
            return
        if not any(cleaned_data and not cleaned_data.get('DELETE', False)
                   for cleaned_data in self.cleaned_data):
            raise forms.ValidationError(
                'Нужно добавить хоть один элемент'
            )


class UnitEditForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = [
            'name',
            'square',
            'description',
            'city',
            'street',
            'build',
            'floor',
            'flat',
            'price'
        ]


class UnitBaseCreateForm(forms.ModelForm):
    c_field = forms.CharField(help_text='Введите город', label='Город')
    s_field = forms.CharField(
        max_length=200, help_text='Введите название улицы', label='Улица')
    b_field = forms.IntegerField(
        help_text='Введите номер строение', label='Строение')
    bl_field = forms.CharField(
        required=False,
        max_length=200, help_text='Введите корпус', label='Корпус')
    f_field = forms.IntegerField(
        required=False, help_text='Введите кол-во этажей', label='Этажей')

    class Meta:
        model = Unit
        fields = [
            'name',
            'square',
            'description',
            'deal',
            'c_field',
            's_field',
            'b_field',
            'bl_field',
            'f_field',
            'floor',
            'flat',
            'price'
        ]
        label = [
            'Название объекта',
            'Площадь, (m2)',
            'Описание',
            'Этаж',
            'Номер помещения',
            'Цена'
        ]
        help_text = [
            'Введите название объекта',
            "Введите площадь",
            "Введите описание объекта"
        ]


class UnitCreateForm(UnitBaseCreateForm):
    images = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        label='Фото')

    class Meta(UnitBaseCreateForm.Meta):
        fields = UnitBaseCreateForm.Meta.fields + ['images']


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Фото', show_hidden_initial=True)

    class Meta:
        model = Image
        fields = ['image']


ImagesFormSet = modelformset_factory(
    Image,
    form=ImageForm,
    max_num=20,
    can_delete=True,
    extra=0
)
