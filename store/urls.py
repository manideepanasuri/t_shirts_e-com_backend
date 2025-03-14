from django.urls import path

from store.views import *

urlpatterns = [
    path('allproducts/',get_products,name='allproducts'),
    path('product/',get_product_id,name='products'),
    path('reviews/',get_reviews,name='reviews'),
    path('wishlist/',WishlistView.as_view(),name='wishlist'),
    path('allcategories/',get_categories,name='allcategories'),
    path('productvariations/',get_variations,name='productvariations'),
    path('variation_details/',get_variations_all,name='variations_all'),
]