from django import forms
from .models import Post, PostImage, Comment


class PostForm(forms.Form):

    caption = forms.CharField(required=True, widget=forms.TextInput(attrs={'class':'form-control mb-2 rounded', 'placeholder':'Write a caption'}))

    class Meta:
        fields = ['caption']


class PostImageForm(forms.Form):

    image = forms.FileField(required=True, widget=forms.ClearableFileInput(attrs={'class':'form-control mb-2 rounded','multiple':True}))

    class Meta:
        fields = ['image']


class CommentForm(forms.ModelForm):

    body = forms.CharField(required=True, widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Add a comment', 'id':'add-comment', 'rows':'1'}))

    class Meta:
        model = Comment
        fields = ['body']