from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm, HiddenInput

from django_project import settings
from .models import Profile, ProfileImage, BasicData, BasicDataModel


class UserRegistrationForm(ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')


class ProfileUpdateImageForm(forms.ModelForm):
    class Meta:
        model = ProfileImage
        fields = ['image']


class ProfileUpdatePNumberForm(forms.ModelForm):
    phone_number = forms.CharField(label='Номер телефона', max_length=20)

    class Meta:
        model = Profile
        fields = ['phone_number']


class BasicDataForm(forms.ModelForm):
    bd_model = forms.ModelChoiceField(queryset=BasicDataModel.objects.all(), widget=HiddenInput())
    name_report = forms.CharField(label='Название отчета об оценке')
    report_number = forms.CharField(label='Номер отчета об оценке')
    date_report = forms.DateField(label='Дата составления отчета (Формат: дд-мм-гггг)',
                                  input_formats=settings.DATE_INPUT_FORMATS)
    basis_for_evaluation = forms.CharField(label='Основание для проведения оценки')
    object_of = forms.CharField(label='Объект оценки')
    composition = forms.CharField(label="Состав объекта оценки", help_text="", widget=forms.Textarea())
    purpose = forms.CharField(label='Цель оценки')
    use_obj = forms.CharField(label='Предполагаемое использование объекта оценки')
    price_type = forms.CharField(label='Вид стоимости')
    date_rent_estimate = forms.DateField(label='Дата оценки (Формат: дд-мм-гггг)',
                                         input_formats=settings.DATE_INPUT_FORMATS)
    date_inspection = forms.DateField(label='Дата обследования объекта оценки (Формат: дд-мм-гггг)',
                                      input_formats=settings.DATE_INPUT_FORMATS)
    range_limits = forms.CharField(label='Границы диапазона РС')
    org_legal_form = forms.CharField(label='Организационно правовая форма', required=False)
    full_name = forms.CharField(label='Полное наименование', required=False)
    OGRN = forms.CharField(label='ОГРН', required=False)
    date_assignment_OGRN = forms.DateField(label='Дата присвоения ОГРН', input_formats=settings.DATE_INPUT_FORMATS,
                                           required=False)
    last_name = forms.CharField(label='Фамилия', required=False)
    first_name = forms.CharField(label='Имя', required=False)
    mid_name = forms.CharField(label='Отчество', required=False)
    identity_document = forms.ImageField(label='Удостоверение личности', required=False)
    location_leg = forms.CharField(label='Адрес места нахождения', required=False)
    location_ind = forms.CharField(label='Адрес места нахождения', required=False)
    documents = forms.CharField(label="Правоустанавливающие документы", help_text="", widget=forms.Textarea())

    class Meta:
        model = BasicData
        fields = "__all__"
