from django import forms
from .models import ClientLead
from django_ckeditor_5.widgets import CKEditor5Widget

class ContactUs(forms.ModelForm):
    message = forms.CharField(widget=CKEditor5Widget(config_name='default'))

    class Meta:
        model = ClientLead
        fields = ['client_name', 'client_email', 'subject', 'message', 'file_supporting_the_message']
        widgets = {
            'client_name': forms.TextInput(attrs={'placeholder': 'Your name'}),
            'client_email': forms.TextInput(attrs={'placeholder': 'Your email'}),
            'subject': forms.TextInput(attrs={'placeholder': 'Subject line'}),
        }