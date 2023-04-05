from django import forms
from .models import Story, StoryReply


class StoryForm(forms.ModelForm):

    caption = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control mb-2 rounded', 'placeholder':'Write a caption'}))
    image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'class': 'form-control rounded mb-2', 'placeholder':'Your story image'}))

    class Meta:
        model = Story
        fields = ['caption', 'image']


class StoryReplyForm(forms.ModelForm):
    body = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control rounded', 'placeholder':'Add your message here...'}))

    class Meta:
        model = StoryReply
        fields = ['body']