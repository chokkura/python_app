from django import forms

from .models import News


class NewNewsForm(forms.ModelForm):
    
    class Meta:
        model = News
        fields = ('title', 'field', 'summary', 'pub_date')


class EditNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title', 'field', 'summary', 'pub_date')