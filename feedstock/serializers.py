from rest_framework import serializers
from .models import Product, Material, ProductMaterial, Warehouse


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'product_code']

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_code']

class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_code']


class MaterialCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'material_name']


class MaterialDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'material_name']


class MaterialListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = ['id', 'material_name']


class ProductMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMaterial
        fields = '__all__'


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'material_id', 'remainder', 'price']
