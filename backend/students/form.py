from django import forms
from .models import students

class studentform(forms.ModelForm):
    class Meta:
        model=students
        fields=[
            'name',
            'email',
            'age',
            'department'
        ]