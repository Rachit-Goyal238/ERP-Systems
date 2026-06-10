from django.urls import path

from . import views

urlpatterns = [

    path(
        '',
        views.product_list,
        name='product_list'
    ),

    path(
        'create/',
        views.product_create,
        name='product_create'
    ),

    path(
        'update/<int:pk>/',
        views.product_update,
        name='product_update'
    ),

    path(
        'delete/<int:pk>/',
        views.product_delete,
        name='product_delete'
    ),

    path(
    'export/',
    views.export_inventory_csv,
    name='export_inventory_csv'
),

path(
    'detail/<int:pk>/',
    views.product_detail,
    name='product_detail'
),

path(
    'transactions/',
    views.transaction_history,
    name='transaction_history'
),
]