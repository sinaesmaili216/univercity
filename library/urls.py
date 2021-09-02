from django.urls import path
from library.views import rent_book, rent_book_list

app_name = 'library'
urlpatterns = [
    path('rent_book/', rent_book, name='rent_book'),
    path('show_rent_books', rent_book_list, name='show_rent_books')
]
