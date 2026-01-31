from django.urls import include, path

from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet, CategoryViewSet, ReviewViewSet
from order.views import CartItemViewSet, CartViewSet, OrderViewSet
from rest_framework_nested import routers

# router = SimpleRouter()
router = DefaultRouter()
router.register("products", ProductViewSet, basename="product")
router.register("categories", CategoryViewSet, basename="category")
router.register("carts", CartViewSet, basename="cart")
router.register("orders", OrderViewSet, basename="order")

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", ReviewViewSet, basename="product-review")

cart_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
cart_router.register("items", CartItemViewSet, basename="cart-item")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls)),
    path("", include(cart_router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
