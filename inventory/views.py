from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from .models import Product
from .forms import ProductForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
import csv

from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import (
    Product,
    InventoryTransaction
)

def inventory_access(user):

    return (
        user.is_superuser
        or
        user.groups.filter(
            name='Inventory Manager'
        ).exists()
    )


@login_required
@user_passes_test(inventory_access)
def export_inventory_csv(request):

    response = HttpResponse(
        content_type='text/csv'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename=inventory.csv'

    writer = csv.writer(
        response
    )

    writer.writerow([

        'Product ID',

        'Name',

        'Quantity',

        'Price'
    ])

    products = Product.objects.all()

    for product in products:

        writer.writerow([

            product.product_id,

            product.product_name,

            product.quantity,

            product.price
        ])

    return response

@login_required
@user_passes_test(inventory_access)
def product_detail(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    return render(
        request,
        'inventory/product_detail.html',
        {
            'product': product
        }
    )


@login_required
@user_passes_test(inventory_access)
def product_list(request):

    query = request.GET.get('search')

    if query:

        product_list = Product.objects.filter(
            product_name__icontains=query
        )

    else:

        product_list = Product.objects.all()

    paginator = Paginator(
        product_list,
        5
    )

    page_number = request.GET.get(
        'page'
    )

    products = paginator.get_page(
        page_number
    )

    return render(
        request,
        'inventory/product_list.html',
        {
            'products': products
        }
    )

@login_required
@user_passes_test(inventory_access)
def product_create(request):

    if request.method == 'POST':

        form = ProductForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                'product_list'
            )

    else:

        form = ProductForm()

    return render(
        request,
        'inventory/product_form.html',
        {
            'form': form
        }
    )

@login_required
@user_passes_test(inventory_access)
def product_update(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    old_quantity = product.quantity

    if request.method == 'POST':

        form = ProductForm(
            request.POST,
            instance=product
        )

        if form.is_valid():

            updated_product = form.save()

            new_quantity = (
                updated_product.quantity
            )

            difference = (
                new_quantity -
                old_quantity
            )

            if difference != 0:

                InventoryTransaction.objects.create(

                    product=updated_product,

                    quantity_changed=abs(
                        difference
                    ),

                    transaction_type=
                    'Added'
                    if difference > 0
                    else 'Removed'
                )

            return redirect(
                'product_list'
            )

    else:

        form = ProductForm(
            instance=product
        )

    return render(
        request,
        'inventory/product_form.html',
        {
            'form': form
        }
    )


@login_required
@user_passes_test(inventory_access)
def transaction_history(request):

    transactions = (
        InventoryTransaction.objects
        .order_by('-created_at')
    )

    return render(
        request,
        'inventory/transaction_history.html',
        {
            'transactions': transactions
        }
    )


@login_required
@user_passes_test(inventory_access)
def product_delete(request, pk):

    product = get_object_or_404(
        Product,
        pk=pk
    )

    product.delete()

    return redirect(
        'product_list'
    )