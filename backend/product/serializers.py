from decimal import Decimal
from rest_framework import serializers
from product.models import Category, Product, Review


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

    product_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "name", "description"]
