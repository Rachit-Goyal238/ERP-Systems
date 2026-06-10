from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from django.db.models import Count

from employee.models import Employee

from inventory.models import (
    Product,
    InventoryTransaction
)

import json

@login_required
def dashboard_v3(request):

    employee_count = Employee.objects.count()

    product_count = Product.objects.count()

    low_stock_count = Product.objects.filter(
        quantity__lt=10
    ).count()

    transaction_count = InventoryTransaction.objects.count()

    recent_employees = Employee.objects.order_by(
        '-id'
    )[:5]

    recent_transactions = InventoryTransaction.objects.order_by(
        '-id'
    )[:5]

    department_stats = Employee.objects.values(
        'department'
    ).annotate(
        total=Count('department')
    )

    department_labels = []
    department_counts = []

    for department in department_stats:

        department_labels.append(
            department['department']
        )

        department_counts.append(
            department['total']
        )

    in_stock_count = Product.objects.filter(
        quantity__gt=10
    ).count()

    low_stock_inventory_count = Product.objects.filter(
        quantity__gt=0,
        quantity__lte=10
    ).count()

    out_of_stock_count = Product.objects.filter(
        quantity=0
    ).count()

    context = {

        'employee_count': employee_count,

        'product_count': product_count,

        'low_stock_count': low_stock_count,

        'transaction_count': transaction_count,

        'recent_employees': recent_employees,

        'recent_transactions': recent_transactions,

        'department_labels':
        json.dumps(department_labels),

        'department_counts':
        json.dumps(department_counts),

        'in_stock_count':
        in_stock_count,

        'low_stock_inventory_count':
        low_stock_inventory_count,

        'out_of_stock_count':
        out_of_stock_count,

        'department_stats':
department_stats,
    }

    return render(
        request,
        'dashboard/dashboard_v3.html',
        context
    )

@login_required
def dashboard(request):

    employee_count = Employee.objects.count()

    product_count = Product.objects.count()

    inventory_value = 0

    for product in Product.objects.all():

        inventory_value += (
            product.quantity *
            product.price
        )

    low_stock_products = Product.objects.filter(
        quantity__lt=10
    )

    low_stock_count = low_stock_products.count()

    recent_employees = Employee.objects.order_by(
        '-id'
    )[:5]

    recent_products = Product.objects.order_by(
        '-id'
    )[:5]

    department_stats = Employee.objects.values(
        'department'
    ).annotate(
        total=Count('department')
    )

    department_labels = []

    department_counts = []

    for department in department_stats:

        department_labels.append(
            department['department']
        )

        department_counts.append(
            department['total']
        )

    in_stock_count = Product.objects.filter(
        quantity__gt=10
    ).count()

    low_stock_inventory_count = Product.objects.filter(
        quantity__gt=0,
        quantity__lte=10
    ).count()

    out_of_stock_count = Product.objects.filter(
        quantity=0
    ).count()

    inventory_status_labels = [

        'In Stock',

        'Low Stock',

        'Out Of Stock'
    ]

    inventory_status_counts = [

        in_stock_count,

        low_stock_inventory_count,

        out_of_stock_count
    ]

    context = {

        'employee_count':
        employee_count,

        'product_count':
        product_count,

        'inventory_value':
        inventory_value,

        'low_stock_count':
        low_stock_count,

        'low_stock_products':
        low_stock_products,

        'recent_employees':
        recent_employees,

        'recent_products':
        recent_products,

        'department_stats':
        department_stats,

        'in_stock_count':
        in_stock_count,

        'out_of_stock_count':
        out_of_stock_count,

        'department_labels':
        json.dumps(
            department_labels
        ),

        'department_counts':
        json.dumps(
            department_counts
        ),

        'inventory_status_labels':
        json.dumps(
            inventory_status_labels
        ),

        'inventory_status_counts':
        json.dumps(
            inventory_status_counts
        ),
    }

    return render(
        request,
        'dashboard/dashboard.html',
        context
    )


@login_required
def dashboard_v2(request):

    employee_count = Employee.objects.count()

    product_count = Product.objects.count()

    inventory_value = 0

    for product in Product.objects.all():

        inventory_value += (
            product.quantity *
            product.price
        )

    low_stock_products = Product.objects.filter(
        quantity__lt=10
    )

    low_stock_count = low_stock_products.count()

    recent_employees = Employee.objects.order_by(
        '-id'
    )[:5]

    recent_products = Product.objects.order_by(
        '-id'
    )[:5]

    recent_transactions = (
        InventoryTransaction.objects
        .order_by('-created_at')[:5]
    )

    department_stats = Employee.objects.values(
        'department'
    ).annotate(
        total=Count('department')
    )

    department_labels = []

    department_counts = []

    for department in department_stats:

        department_labels.append(
            department['department']
        )

        department_counts.append(
            department['total']
        )

    in_stock_count = Product.objects.filter(
        quantity__gt=10
    ).count()

    low_stock_inventory_count = Product.objects.filter(
        quantity__gt=0,
        quantity__lte=10
    ).count()

    out_of_stock_count = Product.objects.filter(
        quantity=0
    ).count()

    transaction_count = (
        InventoryTransaction.objects.count()
    )

    context = {

        'employee_count':
        employee_count,

        'product_count':
        product_count,

        'inventory_value':
        inventory_value,

        'low_stock_count':
        low_stock_count,

        'recent_employees':
        recent_employees,

        'recent_products':
        recent_products,

        'recent_transactions':
        recent_transactions,

        'transaction_count':
        transaction_count,

        'department_labels':
        json.dumps(
            department_labels
        ),

        'department_counts':
        json.dumps(
            department_counts
        ),

        'in_stock_count':
        in_stock_count,

        'low_stock_inventory_count':
        low_stock_inventory_count,

        'out_of_stock_count':
        out_of_stock_count,
    }

    return render(
        request,
        'dashboard/dashboard_v2.html',
        context
    )

