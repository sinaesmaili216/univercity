from django import forms
from .models import Book


class RentBook(forms.ModelForm):
    # email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    # password = forms.CharField(widget=forms.PasswordInput())
    #
    class Meta:
        model = Book
        fields = ['name']
