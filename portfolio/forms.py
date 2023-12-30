from django.forms import ModelForm, TextInput
from .models import ClientLead
from froala_editor.widgets import FroalaEditor
from ckeditor.fields import RichTextField


class ContactUs(ModelForm):
    """
    Stores the client leads submitted using contact us form
    """
    class Meta:
        model = ClientLead
        fields = ['client_name', 'client_email', 'subject', 'message', 'file_supporting_the_message']
        widgets = {
            'client_name': TextInput(attrs={'placeholder': 'Your name'}),
            'client_email': TextInput(attrs={'placeholder': 'Your email'}),
            'subject': TextInput(attrs={'placeholder': 'Subject line'}),
            'message': RichTextField(config_name='default'),
        }