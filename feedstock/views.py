from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from feedstock.models import Product, Material, ProductMaterial, Warehouse
from feedstock.serializers import (
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductListSerializer, MaterialCreateSerializer, MaterialDetailSerializer, MaterialListSerializer,
    ProductMaterialSerializer, WarehouseSerializer
)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .paginations import ProductPagination


class ProductCreateView(APIView):

    @swagger_auto_schema(request_body=ProductCreateSerializer,
                         responses={
                             201: ProductCreateSerializer,
                             400: 'Bad Request'
                         })
    def post(self, request, *args, **kwargs):
        serializer = ProductCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDeleteView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="O‘chiriladigan mahsulot UUID raqami",
                type=openapi.TYPE_STRING,
            )
        ],
        responses={
            204: openapi.Response("Mahsulot o‘chirildi!"),
            404: openapi.Response("Mahsulot topilmadi!"),
        }
    )
    def delete(self, request, *args, **kwargs):
        product_id = kwargs.get('id')
        try:
            product = Product.objects.get(id=product_id)
            product.delete()
            return Response({"detail": "Mahsulot o‘chirildi!"}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({"error": "Mahsulot topilmadi!"}, status=status.HTTP_404_NOT_FOUND)


class ProductDetailView(APIView):

    @swagger_auto_schema(
        operation_description="UUID orqali mahsulot oling",
        responses={
            200: ProductDetailSerializer,
            404: openapi.Response("Mahsulot topilmadi!")
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs.get('id'))
            serializer = ProductDetailSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Mahsulot topilmadi!"}, status=status.HTTP_404_NOT_FOUND)


class ProductListView(APIView):

    @swagger_auto_schema(
        operation_description="Barcha mahsulotlarni yuklab olish",
        responses={
            200: ProductListSerializer(many=True),
            404: openapi.Response("Hech qanday mahsulot topilmadi")
        }
    )
    def get(self, request, *args, **kwargs):
        paginator = ProductPagination()
        products = Product.objects.all().order_by('id')
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductListSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class MaterialCreateView(APIView):
    @swagger_auto_schema(
        request_body=MaterialCreateSerializer,
        responses={
            201: MaterialCreateSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = MaterialCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaterialDetailView(APIView):
    @swagger_auto_schema(
        operation_description="UUID orqali mahsulot oling",
        responses={
            200: MaterialDetailSerializer,
            404: openapi.Response("Material topilmadi!")
        }
    )
    def get(self, request, *args, **kwargs):
        try:
            material = Material.objects.get(id=kwargs.get('id'))
            serializer = MaterialDetailSerializer(material)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Material.DoesNotExist:
            return Response({
                "error": "Material topilmadi!"
            }, status=status.HTTP_404_NOT_FOUND)


class MaterialDeleteView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id',
                              openapi.IN_PATH,
                              description="O'chiriladigan material UUID raqami",
                              type=openapi.TYPE_STRING),
        ],
        responses={
            204: openapi.Response("Material o'chirildi!"),
            404: openapi.Response("Material topilmadi!"),
        }
    )
    def delete(self, request, *args, **kwargs):
        try:
            material = Material.objects.get(id=kwargs.get('id'))
            material.delete()
            return Response({"detail": "Material o‘chirildi!"}, status=status.HTTP_204_NO_CONTENT)
        except Material.DoesNotExist:
            return Response({
                "error": "Material topilmadi!"
            },  status.HTTP_404_NOT_FOUND)


class MaterialListView(APIView):
    @swagger_auto_schema(
        operation_description="Barcha materiallarni yuklab olish",
        responses={
            200: MaterialListSerializer(many=True),
            404: openapi.Response("Hech qanday material topilmadi")
        }
    )
    def get(self, request, *args, **kwargs):
        materials = Material.objects.all().order_by('id')
        serializer = MaterialListSerializer(materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ProductMaterialViewSet(viewsets.ModelViewSet):
    queryset = ProductMaterial.objects.all()
    serializer_class = ProductMaterialSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class ProductMaterialSupplyView(APIView):
    """
    Mahsulotlarni xomashyo bilan ta'minlash APIsi
    """

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'product_code': openapi.Schema(type=openapi.TYPE_INTEGER, description='Mahsulot kodi'),
                'quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description='Buyurtma miqdori'),
            },
            required=['product_code', 'quantity']
        ),
        responses={200: "Mahsulot uchun kerakli xomashyolar va narxlar qaytariladi."}
    )
    def post(self, request):
        product_code = request.data.get('product_code')
        quantity = request.data.get('quantity')

        # Bir nechta mahsulot bo'lishi mumkinligini hisobga olamiz
        products = Product.objects.filter(product_code=product_code)
        if not products.exists():
            return Response({"error": "Mahsulot topilmadi!"}, status=status.HTTP_404_NOT_FOUND)

        result = []

        # Har bir mahsulotni qayta ishlash
        for product in products:
            product_materials = ProductMaterial.objects.filter(product_id=product)
            if not product_materials.exists():
                result.append({
                    "product_name": product.product_name,
                    "product_qty": quantity,
                    "error": "Mahsulot uchun xomashyo ma'lumotlari topilmadi!"
                })
                continue

            total_materials = []

            # Har bir mahsulotga tegishli xomashyo ma'lumotlarini to'plash
            for product_material in product_materials:
                material = product_material.material_id
                required_quantity = product_material.quantity * quantity
                warehouses = Warehouse.objects.filter(material_id=material).order_by('price')
                material_data = []
                material_name = material.material_name
                remaining_qty = required_quantity

                # Ombordagi xomashyoni hisoblash
                for warehouse in warehouses:
                    if remaining_qty <= 0:
                        break

                    if warehouse.remainder > 0:
                        take_qty = min(remaining_qty, warehouse.remainder)
                        material_data.append({
                            "warehouse_id": warehouse.id,
                            "material_name": material_name,
                            "qty": take_qty,
                            "price": float(warehouse.price)
                        })
                        remaining_qty -= take_qty

                # Yetarli xomashyo bo'lmasa, qolgan qismini null bilan qaytarish
                if remaining_qty > 0:
                    material_data.append({
                        "warehouse_id": None,
                        "material_name": material_name,
                        "qty": remaining_qty,
                        "price": None
                    })

                total_materials.extend(material_data)

            # Har bir mahsulotning yakuniy ma'lumotlarini yig'ish
            result.append({
                "product_name": product.product_name,
                "product_qty": quantity,
                "product_materials": total_materials
            })

        return Response({"result": result}, status=status.HTTP_200_OK)

