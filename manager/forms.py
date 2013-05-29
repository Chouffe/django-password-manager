from django import forms
from models import Entry, Category


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ('title', 'url', 'username', 'password', 'comment', 'expires', 'category')
        # widgets = {
        #     'password': forms.PasswordInput(),
        # }


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
