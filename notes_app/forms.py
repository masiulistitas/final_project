from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Note, Category
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class NotesForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)

    class Meta:
        model = Note
        fields = ['category', 'title', 'content', 'image']
        labels = {
            'category': 'Category(not required)',
        }

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Category...'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your title...'}),
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Note...'}),
        }


class CategoryForm(forms.ModelForm):

    def clean(self):
        try:
            Category.objects.get(name=self.cleaned_data['name'])
            raise forms.ValidationError("Exists already!")
        except Category.DoesNotExist:
            pass
        return self.cleaned_data

    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': '',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Category name..'}),
        }
