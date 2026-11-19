from django.shortcuts import render
from .form import studentform

def student_form(request):
    form = studentform()
    return render(request, 'student/student_form.html', {'form': form})