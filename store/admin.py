from django.contrib import admin
from .models import *
# Register your models here.


class VariationImageInline(admin.StackedInline):  # or admin.StackedInline
    model = VariationImage
    extra = 0 # Number of empty forms to display by default

# Inline for Product Variations
class ProductVariationInline(admin.StackedInline):
    model = ProductVariation
    extra = 0
    inlines = [VariationImageInline]  # Nested inline for variation images

    # Optionally, customize the fields displayed in the inline form
    fields = ('price', 'stock_quantity','image_preview')
    readonly_fields = ('image_preview',)

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    fields = ('user','rating','comment',)
    sortable_by = ('created_at','rating')

admin.site.register(Review)

# Admin for Product Variation
@admin.register(ProductVariation)
class ProductVariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'stock_quantity','image_preview')
    list_filter = ('product',)
    search_fields = ('product__name',)
    inlines = [VariationImageInline]  # Add variation images as inline forms

# Admin for Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'created_at','image_preview')
    list_filter = ('categories',)
    search_fields = ('name', 'description')
    filter_horizontal = ('categories',)  # Adds a user-friendly widget for managing categories
    inlines = [ProductVariationInline,ReviewInline]  # Add variations as inline forms

# Admin for Variation Image
@admin.register(VariationImage)
class VariationImageAdmin(admin.ModelAdmin):
    list_display = ('variation', 'image', 'alt_text','image_preview')
    readonly_fields = ('image_preview',)  # Make the preview field read-only
    list_filter = ('variation__product',)
    search_fields = ('variation__product__name',)

# Admin for Attributes and Attribute Values
class AttributeValueInline(admin.TabularInline):
    model = AttributeValue
    extra = 1

@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [AttributeValueInline]

@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ('attribute', 'value')
    list_filter = ('attribute',)
    search_fields = ('value',)

# Admin for Category
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Wishlist)
