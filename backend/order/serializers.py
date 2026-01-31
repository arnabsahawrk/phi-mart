from typing import Any, Dict, cast

from rest_framework import serializers
from order.models import Cart, CartItem, Order, OrderItem
from order.services import OrderService
from product.models import Product


class EmptySerializer(serializers.Serializer):
    pass


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price"]


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product"
    )

    class Meta:
        model = CartItem
        fields = ["id", "product_id", "quantity"]

    def save(self, **kwargs):
        validated_data = cast(Dict[str, Any], self.validated_data)
        cart_id = self.context["cart_id"]
        product = validated_data.get("product")
        if product is None:
            raise serializers.ValidationError({"product_id": "This field is required."})
        quantity = validated_data["quantity"]

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, product=product, quantity=quantity
            )

        return self.instance


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.price * cart_item.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total_price"]
        read_only_fields = ["user"]

    def get_total_price(self, cart):
        return sum([item.product.price * item.quantity for item in cart.items.all()])


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        user_id = self.context["user_id"]

        if not Cart.objects.filter(pk=cart_id, user_id=user_id).exists():
            raise serializers.ValidationError("No cart found with this id")
        elif not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError("Cart is empty")
        return cart_id

    def create(self, validated_data):
        user_id = self.context["user_id"]
        cart_id = validated_data["cart_id"]

        try:
            order = OrderService.create_order(user_id=user_id, cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        return OrderSerializer(instance).data


class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ["id", "product", "price", "quantity", "total_price"]


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]

    """ def update(self, instance, validated_data):
        user = self.context["user"]
        status = validated_data["status"]

        if status == Order.CANCELED:
            return OrderService.cancel_order(order=instance, user=user)

        if not user.is_staff:
            raise serializers.ValidationError(
                {"message": "You are not allowed to update this order"}
            )

        return super().update(instance, validated_data) """


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "items",
            "status",
            "total_price",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["items"]
