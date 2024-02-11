from django import forms

from blogapp.models import Comments


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    comments = forms.CharField(required=False, widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('username', 'body', 'email')


class SearchForm(forms.Form):
    query = forms.CharField()