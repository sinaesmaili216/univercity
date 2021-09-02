from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from faculty.models import Class, Student, Lesson, Master, User
from .forms import CreateStudent, SelectLesson, LoginForm, EditLessonsByMaster, RegisterMaster
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'faculty/index.html')


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

        user = authenticate(email=email, password=password)

        if user:
            login(request, user)
            return render(request, 'faculty/index.html')
        else:
            return HttpResponse('email or password is incorrect')
    else:
        form = LoginForm()

    return render(request, 'faculty/login.html', context={'form': form})


def logout_user(request):
    logout(request)
    return redirect('faculty:login')


def show_class_list(request):
    classes = Class.objects.all()
    context = {
        'classes': classes
    }
    return render(request, 'faculty/class_lists.html', context)


def search_in_class_list(request):
    search_word = request.POST['search']

    class_name = Class.objects.filter((Q(name__contains=search_word) | Q(lessons__name__contains=search_word)))

    if class_name:
        students = class_name.get().students.all
        lessons = class_name.get().lessons.all
        context = {
            'lessons': lessons,
            'students': students
        }
    else:
        return HttpResponseRedirect('faculty:class_list')

    return render(request, 'faculty/class_info.html', context)


def class_info(request, name):
    class_name = Class.objects.get(name=name)
    lessons = class_name.lessons.all
    students = class_name.students.all
    context = {
        'lessons': lessons,
        'students': students
    }
    return render(request, 'faculty/class_info.html', context)


def create_student(request):
    if request.method == 'POST':
        form = CreateStudent(request.POST)
        if form.is_valid():
            nation_code = form['nation_code'].value()
            student = Student.objects.filter(nation_code=nation_code)
            if student:
                return HttpResponse('this student is exist')
            else:
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')
                create_new_user = User.objects.create_user(email=email, password=password)
                create_new_user.is_student = True
                create_new_user.save()
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                nation_code = form.cleaned_data.get('nation_code')
                age = form.cleaned_data.get('age')
                faculty = form.cleaned_data.get('faculty')
                phone = form.cleaned_data.get('phone')
                print(phone)
                new_student = Student.objects.create(first_name=first_name, last_name=last_name, nation_code=nation_code, age=age, user=create_new_user, faculty=faculty, phone=phone)
                new_student.save()
                login(request, create_new_user)
                return redirect('faculty:index')
    else:
        form = CreateStudent()

    return render(request, 'faculty/create_student.html', context={'form': form})


def select_lesson(request):
    if request.method == 'POST':
        form = SelectLesson(request.POST)
        if form.is_valid():
            lessons = form.cleaned_data.get('lessons')
            student = Student.objects.get(user=request.user)
            [student.lessons.add(Lesson.objects.get(name=lesson)) for lesson in lessons]
            return HttpResponse('lesson added')
    else:
        form = SelectLesson()

    return render(request, 'faculty/select_lesson.html', context={'form': form})


def students_list(request):
    all_students = Student.objects.all()
    return render(request, 'faculty/students_list.html', context={'students': all_students})


def edit_student_lessons_by_master(request, student_name):
    student = Student.objects.get(first_name=student_name)
    if request.method == 'POST':
        form = EditLessonsByMaster(request.POST)
        if form.is_valid():
            lessons = form.cleaned_data.get('lessons')
            for lesson in lessons:
                lesson = Lesson.objects.get(name=lesson)
                student.lessons.add(lesson)
            return HttpResponse('changes saved')
    else:
        form = EditLessonsByMaster()

    return render(request, 'faculty/edit_lesson_by_master.html', context={'student': student, 'form': form})


def register_master(request):
    if request.method == 'POST':
        form = RegisterMaster(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            new_user = User.objects.create_user(email=email, password=password)
            new_user.is_teacher = True
            new_user.save()

            create_new_master = Master.objects.create(user=new_user, first_name=first_name, last_name=last_name)
            create_new_master.save()

            login(request, new_user)
            return redirect('faculty:index')
    else:
        form = RegisterMaster()

    return render(request, 'faculty/register_master.html', context={'form': form})
