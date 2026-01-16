from django.urls import include, path

from rest_framework.routers import DefaultRouter
from product import views
from rest_framework_nested import routers

# router = SimpleRouter()
router = DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("categories", views.CategoryViewSet)

product_router = routers.NestedDefaultRouter(router, "products", lookup="product")
product_router.register("reviews", views.ReviewViewSet, basename="product-review")


urlpatterns = [
    path("", include(router.urls)),
    path("", include(product_router.urls)),
]
