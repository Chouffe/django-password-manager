from django import forms
from models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('title', 'url', 'username', 'comment', 'expires')
