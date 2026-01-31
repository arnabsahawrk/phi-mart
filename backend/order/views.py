from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)

from order.models import Cart, CartItem, Order
from order.serializers import (
    CartItemSerializer,
    CartSerializer,
    AddCartItemSerializer,
    CreateOrderSerializer,
    EmptySerializer,
    OrderSerializer,
    UpdateCartItemSerializer,
    UpdateOrderSerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action

from order.services import OrderService


class CartViewSet(
    CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.prefetch_related("items__product").filter(
            user=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer

        return CartItemSerializer

    def get_serializer_context(self):
        return {**super().get_serializer_context(), "cart_id": self.kwargs["cart_pk"]}

    def get_queryset(self):
        return CartItem.objects.select_related("product").filter(
            cart_id=self.kwargs["cart_pk"]
        )

    def perform_create(self, serializer):
        cart = get_object_or_404(Cart, pk=self.kwargs["cart_pk"])
        serializer.save(cart=cart)

    def perform_update(self, serializer):
        cart = get_object_or_404(Cart, pk=self.kwargs["cart_pk"])
        serializer.save(cart=cart)


class OrderViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        OrderService.cancel_order(order=self.get_object(), user=request.user)
        return Response({"status": "Order canceled"})

    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        serializer = UpdateOrderSerializer(
            self.get_object(), data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"status": f"Order status updated to {request.data["status"]}"})

    def get_permissions(self):
        if self.action in ["update_status", "destroy"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == "cancel":
            return EmptySerializer
        elif self.action == "create":
            return CreateOrderSerializer
        elif self.action == "update_status":
            return UpdateOrderSerializer
        return OrderSerializer

    def get_serializer_context(self):
        return {"user_id": self.request.user.pk, "user": self.request.user}

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.prefetch_related("items__product").all()
        return Order.objects.prefetch_related("items__product").filter(
            user=self.request.user
        )
