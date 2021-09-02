from django.contrib import admin
from library.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    filter = ['name', 'code']
    list_display = ['name', 'code', 'course', 'student_who_rent']
