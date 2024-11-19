from django.db import models
import uuid


class Product(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    product_name = models.CharField(max_length=255)
    product_code = models.IntegerField()


    def __str__(self):
        return self.product_name


class Material(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    material_name = models.CharField(max_length=255)


class ProductMaterial(models.Model):
    id = models.UUIDField(
        primary_key= True,
        default=uuid.uuid4,
        editable=False
    )
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.IntegerField()


class Warehouse(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    material_id = models.ForeignKey(Material, on_delete=models.CASCADE)
    remainder = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=0)