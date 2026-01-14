from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from product.serializers import ProductSerializer, CategorySerializer
from rest_framework import status
from django.db.models import Count
from product.models import Category, Product


@api_view(["GET", "POST"])
def view_products(request):
    if request.method == "GET":
        products = Product.objects.select_related("category").all()
        serializers = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializers.data)
    elif request.method == "POST":
        deserializer = ProductSerializer(
            data=request.data, context={"request": request}
        )
        deserializer.is_valid(raise_exception=True)
        print(deserializer.validated_data)
        deserializer.save()
        return Response(deserializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"request": "Invalid"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def view_specific_product(request, pk):
    if request.method == "GET":
        product = get_object_or_404(Product, pk=pk)
        serializers = ProductSerializer(product, context={"request": request})
        return Response(serializers.data)
    elif request.method == "PUT":
        product = get_object_or_404(Product, pk=pk)
        serializers = ProductSerializer(
            product, data=request.data, context={"request": request}
        )
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)
    elif request.method == "DELETE":
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        return Response({"request": "Invalid"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "POST"])
def view_categories(request):
    if request.method == "GET":
        categories = Category.objects.annotate(product_count=Count("products")).all()
        serializers = CategorySerializer(categories, many=True)
        return Response(serializers.data)
    elif request.method == "POST":
        deserializer = CategorySerializer(data=request.data)
        if deserializer.is_valid():
            print(deserializer.validated_data)
            deserializer.save()
            return Response(deserializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(deserializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"request": "Invalid"}, status=status.HTTP_400_BAD_REQUEST)


@api_view()
def view_specific_category(request, pk):
    category = get_object_or_404(
        Category.objects.annotate(product_count=Count("products")), pk=pk
    )
    serializers = CategorySerializer(category)
    return Response(serializers.data)
