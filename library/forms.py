from django import forms
from django.core.exceptions import ValidationError
from faculty.models import Student
from .models import Book


class RentBook(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get('name')
        book = Book.objects.get(name=name)

        if book.student_who_rent:
            raise ValidationError('This book was rented by another student')
        return cleaned_data

    class Meta:
        model = Book
        fields = ['name', 'end_date_rent']


class DeliverBook(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name']
