from django.db import models

# Create your models here.
class Product(models.Model):

    product_id = models.CharField(max_length=20)

    product_name = models.CharField(max_length=100)

    quantity = models.IntegerField()

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    supplier = models.CharField(max_length=100)

class InventoryTransaction(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity_changed = models.IntegerField()

    transaction_type = models.CharField(
        max_length=20
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):

        return (
            f"{self.product.product_name}"
            f" - "
            f"{self.transaction_type}"
        )