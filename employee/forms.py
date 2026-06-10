from django import forms
from .models import Employee

class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee

        fields = [
            'employee_id',
            'name',
            'email',
            'phone',
            'department',
            'designation',
            'salary',
            'joining_date'
        ]

        widgets = {
            'joining_date': forms.DateInput(
                attrs={'type': 'date'}
            )
        }