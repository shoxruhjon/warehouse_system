from itertools import product

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from feedstock.models import Product
from feedstock.serializers import ProductSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProductCreateView(APIView):

    @swagger_auto_schema(
        request_body=ProductSerializer,
        responses = {201: ProductSerializer}
    )
    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data)
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
            200: ProductSerializer,
            404: openapi.Response("Mahsulot topilmadi!")
        }
    )
    def get(self, request, *arg, **kwargs):
        try:
            product = Product.objects.get(id=kwargs.get('id'))
            serializer = ProductSerializer(product)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"error": "Mahsulot topilmadi!"}, status=status.HTTP_404_NOT_FOUND)


class ProductListView(APIView):

    @swagger_auto_schema(
        operation_description="Barcha mahsulotlarni yuklab olish",
        responses={
            200: ProductSerializer(many=True),
            404: openapi.Response("Hech qanday mahsulot topilmadi")
        }
    )
    def get(self, request, *args, **kwargs):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)