from decimal import Decimal
from rest_framework import serializers
from product.models import Category, Product, ProductImage, Review
from django.contrib.auth import get_user_model


""" class CategorySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    description = serializers.CharField()


class ProductSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    unit_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="price"
    )

    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    # category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    # category = serializers.StringRelatedField()
    # category = CategorySerializer()
    category = serializers.HyperlinkedRelatedField(
        queryset=Category.objects.all(), view_name="specific-category"
    )

    def calculate_tax(self, product):
        return round(product.price * Decimal(1.1), 2) """


class CategorySerializer(serializers.ModelSerializer):
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        fields = "__all__"

    product_count = serializers.IntegerField(
        read_only=True, help_text="Return the number of product in this category"
    )


class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ProductImage
        fields = ["id", "image"]


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "description",
            "price",
            "price_with_tax",
            "stock",
            "category",
            "category_detail",
            "images",
        ]

    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    category_detail = serializers.HyperlinkedRelatedField(
        view_name="category-detail",
        source="category",
        read_only=True,
    )
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product):
        return round(product.price * Decimal(1.1), 2)

    def validate_price(self, price):
        if price < 0:
            raise serializers.ValidationError("Price could not be negative")
        return price


class SimpleUserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(method_name="get_current_user_name")

    class Meta:
        model = get_user_model()
        fields = ["id", "name"]

    def get_current_user_name(self, name):
        return name.get_full_name()


class ReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            "id",
            "product",
            "user",
            "ratings",
            "comment",
            "updated_at",
            "created_at",
        ]
        read_only_fields = ["product", "user"]
