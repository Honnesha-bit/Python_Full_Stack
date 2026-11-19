from django.shortcuts import render, redirect
from .form import studentform
from .models import students


def student_form(request):

    if request.method == 'POST':

        form = studentform(request.POST)

        if form.is_valid():
            form.save()
            return redirect('student_list')

    else:
        form = studentform()

    return render(
        request,
        'student/student_form.html',
        {'form': form}
    )


def student_list(request):

    students = students.objects.all()

    return render(
        request,
        'student/student_list.html',
        {'students': students}
    )