from django.contrib import admin
from .models import (
    Product,
    ProductMaterial,
    Material,
    Warehouse
)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'product_code')
    search_fields = ('id', )


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'material_name')
    search_fields = ('id', 'material_name')


class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_id', 'material_id', 'quantity')
    search_fields = ('id', 'quantity')


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'material_id', 'remainder', 'price')
    search_fields = ('id', 'remainder', 'price')


admin.site.register(Product, ProductAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(ProductMaterial, ProductMaterialAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
