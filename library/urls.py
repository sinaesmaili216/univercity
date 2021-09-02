from django.urls import path
from library.views import rent_book, rent_book_list, deliver_book


app_name = 'library'
urlpatterns = [
    path('rent_book/', rent_book, name='rent_book'),
    path('show_rent_books/', rent_book_list, name='show_rent_books'),
    path('deliver_book/', deliver_book, name='deliver_book')
]
