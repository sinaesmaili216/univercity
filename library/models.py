from django.db import models
from faculty.models import Course, Student
import datetime


class Book(models.Model):
    name = models.CharField(max_length=100)
    code = models.PositiveSmallIntegerField()
    start_date_rent = models.DateTimeField(default=datetime.date.today())
    end_date_rent = models.DateTimeField(default=datetime.date.today())
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
    student_who_rent = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
