from django import forms

from user.models import User
from user.models import Profile


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'sex', 'birthday', 'location']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


    def clean_max_distance(self):
        '''手动清洗和验证max_distance'''
        cleaned = super().clean()
        if cleaned['max_distance'] < cleaned['min_distance']:
            raise forms.ValidationError('max_distance必须大于min_distance')
        else:
            return cleaned['max_distance']



    def clean_max_dating_age(self):
        '''手动清洗和验证max_dating_age'''
        cleaned = super().clean()
        if cleaned['max_dating_age'] < cleaned['min_dating_age']:
            raise forms.ValidationError('max_dating_age必须大于min_dating_age')
        else:
            return cleaned['max_dating_age']