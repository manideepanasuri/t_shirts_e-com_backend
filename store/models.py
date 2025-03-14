from django.contrib.auth import get_user_model
from django.db import models
from django.utils.html import format_html


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Attribute(models.Model):
    """
    Represents an attribute type, such as 'Color' or 'Size'.
    """
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    """
    Represents a specific value for an attribute, such as 'Red' or 'Large'.
    """
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.attribute.name}: {self.value}"



class ProductVariation(models.Model):
    """
    Represents a specific variation of a product, such as 'Red - Large'.
    """
    product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='variations')
    attributes = models.ManyToManyField('AttributeValue')  # Links to specific attribute values
    price = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)

    def __str__(self):
        attributes = ', '.join([str(attr) for attr in self.attributes.all()])
        return f"{self.product.name} ({attributes})"
    def image_preview(self):
        images=self.images.all().first()
        if images:
            return format_html('<img src="{}" width="50" height="50" />', images.image.url)
        return 'No image'


class VariationImage(models.Model):
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(blank=False,null=False,upload_to='variation_images')  # URL of the image
    alt_text = models.CharField(max_length=255, blank=True, null=True)  # Alt text for accessibility

    def __str__(self):
        return f"Image for {self.variation}"

    def image_preview(self):
        if self.image:
            return format_html('<img src="{}" width="50" height="50" />', self.image.url)
        return "No Image"

    image_preview.short_description = 'Preview'  # Column header in the admin panel

# Update the Product model to include a reference to variations
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=0)  # Base price
    categories = models.ManyToManyField('Category',blank=True,related_name='products')
    image = models.ImageField(blank=True, null=True,upload_to="product_images/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def image_preview(self):
        if self.image:
            return format_html('<img src="{}" width="50" height="50" />', self.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

User=get_user_model()
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.name} for {self.product.name}"

    def user_name(self):
        return self.user.name


class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='wishlists')
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='wishlist')
    def __str__(self):
        return f"Wishlist {self.user.name} for {self.product.name}"
