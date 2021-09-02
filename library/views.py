from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import render, redirect

from faculty.models import User, Student
from library.forms import RentBook
from library.models import Book




def rent_book(request):
    if request.method == 'POST':
        form = RentBook(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            student_who_rent_this_book = Student.objects.filter(books__name=name)
            if student_who_rent_this_book:
                return HttpResponse('this book has rent by another student')
            else:
                student = Student.objects.get(user=request.user)
                book = Book.objects.get(name=name)
                student.books.add(book)
                return redirect('library:show_rent_books')
                #return HttpResponse('book rented successfully')
    else:
        form = RentBook()

    return render(request, 'library/rent_book.html', context={'form': form})


def rent_book_list(request):
    student = Student.objects.get(user=request.user)
    books = student.books.all
    return render(request, 'library/rent_books_list.html', context={'books': books, 'user': student})
