from django import forms

class VideoSearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=200)

from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
