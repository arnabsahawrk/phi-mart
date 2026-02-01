from django.db import models
from django.conf import settings
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator,
)

from product.validators import validate_file_size


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="products"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(
        upload_to="product/images/",
        validators=[
            FileExtensionValidator(allowed_extensions=["png", "jpg", "jpeg"]),
            validate_file_size,
        ],
    )


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ratings = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    updated_at = models.DateField(auto_now=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Review by {self.user.email} on {self.product.name}"


"""
Step to build an API
# Model
# Serializer
# ViewSet
# Router
"""
