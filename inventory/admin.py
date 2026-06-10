from django.contrib import admin
from .models import Product
from .models import InventoryTransaction

admin.site.register(
    InventoryTransaction
)
admin.site.register(Product)
