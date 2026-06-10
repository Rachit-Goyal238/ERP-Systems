from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import Employee
from .forms import EmployeeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import csv

from django.http import HttpResponse
from django.core.paginator import Paginator


def employee_access(user):

    return (
        user.is_superuser
        or
        user.groups.filter(
            name='HR'
        ).exists()
    )

@login_required
@user_passes_test(employee_access)
def export_employees_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename=employees.csv'

    writer = csv.writer(
        response
    )

    writer.writerow([
        'Employee ID',
        'Name',
        'Department',
        'Designation'
    ])

    employees = Employee.objects.all()

    for employee in employees:

        writer.writerow([

            employee.employee_id,

            employee.name,

            employee.department,

            employee.designation
        ])

    return response


@login_required
@user_passes_test(employee_access)
def employee_list(request):

    query = request.GET.get('search')

    if query:

        employee_list = Employee.objects.filter(
            name__icontains=query
        )

    else:

        employee_list = Employee.objects.all()

    paginator = Paginator(
        employee_list,
        5
    )

    page_number = request.GET.get('page')

    employees = paginator.get_page(
        page_number
    )

    return render(
        request,
        'employee/employee_list.html',
        {
            'employees': employees
        }
    )


@login_required
@user_passes_test(employee_access)
def employee_create(request):

    if request.method == 'POST':

        form = EmployeeForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('employee_list')

    else:

        form = EmployeeForm()

    return render(
        request,
        'employee/employee_form.html',
        {
            'form': form
        }
    )

@login_required
@user_passes_test(employee_access)
def employee_update(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    if request.method == 'POST':

        form = EmployeeForm(
            request.POST,
            instance=employee
        )

        if form.is_valid():

            form.save()

            return redirect(
                'employee_list'
            )

    else:

        form = EmployeeForm(
            instance=employee
        )

    return render(
        request,
        'employee/employee_form.html',
        {
            'form': form
        }
    )

@login_required
@user_passes_test(employee_access)
def employee_delete(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    employee.delete()

    return redirect(
        'employee_list'
    )

@login_required
@user_passes_test(employee_access)
def employee_detail(request, pk):

    employee = get_object_or_404(
        Employee,
        pk=pk
    )

    return render(
        request,
        'employee/employee_detail.html',
        {
            'employee': employee
        }
    )