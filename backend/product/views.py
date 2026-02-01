from django.shortcuts import get_object_or_404

# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from api.permissions import IsAdminOrReadOnly
from product.permissions import IsReviewAuthorOrReadOnly
from product.serializers import (
    ProductImageSerializer,
    ProductSerializer,
    CategorySerializer,
    ReviewSerializer,
)

# from rest_framework import status
from django.db.models import Count
from product.models import Category, Product, ProductImage, Review

# from rest_framework.views import APIView
# from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from product.filters import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from product.paginations import DefaultPagination
from drf_yasg.utils import swagger_auto_schema

# from rest_framework.permissions import IsAdminUser, AllowAny, SAFE_METHODS, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly


""" @api_view(["GET", "POST"])
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
        return Response({"request": "Invalid"}, status=status.HTTP_400_BAD_REQUEST) """


""" class ViewProducts(APIView):
    def get(self, request):
        products = Product.objects.select_related("category").all()
        serializers = ProductSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        deserializer = ProductSerializer(
            data=request.data, context={"request": request}
        )
        deserializer.is_valid(raise_exception=True)
        deserializer.save()
        return Response(deserializer.data, status=status.HTTP_201_CREATED) """


""" class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related("category")
    serializer_class = ProductSerializer

    # def get_queryset(self):
    #     return Product.objects.select_related("category").all()

    # def get_serializer_class(self):
    #     return ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request} """


""" @api_view(["GET", "PUT", "DELETE"])
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
        return Response({"request": "Invalid"}, status=status.HTTP_400_BAD_REQUEST) """


""" class ViewSpecificProduct(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializers = ProductSerializer(product, context={"request": request})
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializers = ProductSerializer(
            product, data=request.data, context={"request": request}
        )
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) """


""" class ProductDetails(RetrieveUpdateDestroyAPIView):
    queryset = Product
    serializer_class = ProductSerializer """


""" @api_view(["GET", "POST"])
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
        return Response({"request": "Invalid"}, status=status.HTTP_400_BAD_REQUEST) """


class ProductViewSet(ModelViewSet):
    """
    API endpoint for managing products in the e-commerce store
    - Allow authenticated admin to create, update, and delete products
    - Allows users to browse and filter product
    - Support searching name, description, and category
    - Support ordering by price and updated_at
    """

    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ["category_id"]
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "updated_at"]
    pagination_class = DefaultPagination
    # permission_classes = [IsAdminUser]
    permission_classes = [IsAdminOrReadOnly]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    @swagger_auto_schema(operation_summary="Retrieve a list of products")
    def list(self, request, *args, **kwargs):
        """Retrieve all the products"""
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create a product by admin",
        operation_description="This allow admin to create a product",
        request_body=ProductSerializer,
        responses={201: ProductSerializer, 400: "Bad Request"},
    )
    def create(self, request, *args, **kwargs):
        """Only authenticated admin can create product"""
        return super().create(request, *args, **kwargs)

    """ def get_permissions(self):
        # if self.request.method == "GET":
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAdminUser()] """

    """ def get_queryset(self):
        queryset = self.queryset
        request = cast(Request, self.request)
        id = request.query_params.get("category_id")

        if id:
            return queryset.filter(category_id=id)
        else:
            return queryset.all() """


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return ProductImage.objects.none()
        if not self.kwargs.get("product_pk"):
            return ProductImage.objects.none()
        product = get_object_or_404(Product, pk=self.kwargs.get("product_pk"))
        return ProductImage.objects.filter(product=product)

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs.get("product_pk"))
        serializer.save(product=product)


""" class ViewCategories(APIView):
    def get(self, request):
        categories = Category.objects.annotate(product_count=Count("products")).all()
        serializers = CategorySerializer(categories, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        deserializer = CategorySerializer(data=request.data)
        deserializer.is_valid(raise_exception=True)
        deserializer.save()
        return Response(deserializer.data, status=status.HTTP_201_CREATED) """


""" class CategoryList(ListCreateAPIView):
    queryset = Category.objects.annotate(product_count=Count("products"))
    serializer_class = CategorySerializer """


""" @api_view()
def view_specific_category(request, pk):
    category = get_object_or_404(
        Category.objects.annotate(product_count=Count("products")), pk=pk
    )
    serializers = CategorySerializer(category)
    return Response(serializers.data) """


""" class ViewSpecificCategory(APIView):
    def get(self, request, pk):
        category = get_object_or_404(
            Category.objects.annotate(product_count=Count("products")), pk=pk
        )

        serializers = CategorySerializer(category)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializers = CategorySerializer(category, data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) """


""" class CategoryDetails(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.annotate(product_count=Count("products"))
    serializer_class = CategorySerializer """


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(product_count=Count("products"))
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewAuthorOrReadOnly]

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Review.objects.none()
        if not self.kwargs.get("product_pk"):
            return Review.objects.none()
        product = get_object_or_404(Product, pk=self.kwargs.get("product_pk"))
        return Review.objects.filter(product=product)

    def perform_create(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs.get("product_pk"))
        serializer.save(user=self.request.user, product=product)

    def perform_update(self, serializer):
        product = get_object_or_404(Product, pk=self.kwargs.get("product_pk"))
        serializer.save(user=self.request.user, product=product)
