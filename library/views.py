from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect
from faculty.models import User, Student
from library.forms import RentBook, DeliverBook
from library.models import Book


def rent_book(request):
    books_can_rent = Book.objects.filter(student_who_rent=None)  # to show the user to make it easier to select

    if request.method == 'POST':
        form = RentBook(request.POST)
        if form.is_valid():

            name = form.cleaned_data.get('name')
            book = Book.objects.get(name=name)
            if not book.student_who_rent:
                student = Student.objects.get(user=request.user)
                book.student_who_rent = student
                end_date_rent = form.cleaned_data.get('end_date_rent')
                book.end_date_rent = end_date_rent
                book.save()
                return redirect('library:show_rent_books')

    else:
        form = RentBook()

    return render(request, 'library/rent_book.html', context={'form': form, 'books_can_rent': books_can_rent})


def rent_book_list(request):
    student = Student.objects.get(user=request.user)
    books = Book.objects.filter(student_who_rent=student)
    return render(request, 'library/rent_books_list.html', context={'books': books, 'user': student})


def deliver_book(request):
    """ this view is for deliver book after ending deadline """
    if request.method == 'POST':
        form = DeliverBook(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            book = Book.objects.get(name=name)
            book.student_who_rent = None
            book.save()
            return redirect('library:show_rent_books')
    else:
        form = DeliverBook()

    return render(request, 'library/deliver_book.html', context={'form': form})
