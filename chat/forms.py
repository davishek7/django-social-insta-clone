from django import forms
from .models import Inbox, Message


class MessageForm(forms.ModelForm):

    body = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'ms-2 form-control form-control-sm rounded-5', 'placeholder':'Message...'}))
    # image = forms.FileField(widget=forms.ClearableFileInput(attrs={'class':'form-control mb-2 rounded'}))

    class Meta:
        model = Message
        fields = ['body', 'image']