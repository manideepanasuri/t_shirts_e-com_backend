import json

from attr import attributes
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from store.models import Product, Category, ProductVariation, Review, Wishlist
from store.serializers import ProductSerializer, CategorySerializer, ProductVariationSerializer, \
    VariationImageSerializer, AttributeValueSerializer, ReviewSerializer, WishlistSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def get_products(request):
    products = ProductSerializer(Product.objects.all(), many=True).data
    data={
        'success': True,
        'message': 'success',
        'data': products
    }
    return Response(data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_product_id(request):
    id=request.query_params.get('id')
    if not id:
        data={
            'success': False,
            'message': 'id is required',
        }
        return Response(data,status=status.HTTP_400_BAD_REQUEST)
    product=Product.objects.get(id=id)
    data={
        'success': True,
        'message': 'success',
        'data':ProductSerializer(product).data
    }
    return Response(data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_categories(request):
    categories = CategorySerializer(Category.objects.all().order_by("name"), many=True).data
    return Response(categories,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_variations(request):
    product_id=request.query_params.get('product_id')
    print(product_id)
    if product_id is not None:
        if not Product.objects.filter(id=product_id).exists():
            return Response({'message':'Product not found'},status=status.HTTP_404_NOT_FOUND)
        product=Product.objects.get(id=product_id)
        product_variations=ProductVariationSerializer(product.variations.all(), many=True).data
        data={
            'success': True,
            'message': 'success',
            'data': product_variations
        }
        return Response(data,status=status.HTTP_200_OK)
    else:
        data={
            'success': False,
            'message': 'product_id is required',
        }
        return Response(data,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_variations_all(request):
    product_var_id=request.query_params.get('product_variation_id')
    if product_var_id is None:
        return Response('invalid Product variation id',status=status.HTTP_400_BAD_REQUEST)
    if not ProductVariation.objects.filter(id=product_var_id).exists():
        return Response('invalid Product variation id',status=status.HTTP_400_BAD_REQUEST)
    product=ProductVariation.objects.get(id=product_var_id)
    images=VariationImageSerializer(product.images.all(), many=True).data
    attr=AttributeValueSerializer(product.attributes.all(), many=True).data
    return Response({"attributes":attr, "images":images}, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_reviews(request):
    product_id=request.query_params.get('product_id')
    if product_id is None:
        data={
            'success': False,
            'message': 'product_id is required',
        }
        return Response(data,status=status.HTTP_400_BAD_REQUEST)
    else:
        product=Product.objects.get(id=product_id)
        reviews=product.reviews.all().order_by('-created_at')
        data={
            'success': True,
            'message': 'success',
            'data': ReviewSerializer(reviews,many=True).data
        }
        return Response(data,status=status.HTTP_200_OK)

class WishlistView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        user=request.user
        try:
            wishlist=user.wishlist.all()
            data={
                'success': True,
                'message': 'success',
                'data': WishlistSerializer(wishlist, many=True).data
            }
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            data={
                'success': False,
                'message': str(e),
                'data': None
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
    def post(self, request):
        user=request.user
        id=request.data.get('product_id')
        if not Product.objects.filter(id=id).exists():
            data={
                'success': False,
                'message': 'id is required',
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        product=Product.objects.get(id=id)
        if Wishlist.objects.filter(product=product,user=user).exists():
            data={
                'success': False,
                'message': 'product is already wishlisted',
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        try:
            wishlist=Wishlist.objects.create(product=product, user=user)
            data={
                'success': True,
                'message': 'success',
            }
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            data={
                'success': False,
                'message': str(e),
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user=request.user
        id=request.query_params.get('id')
        if not Product.objects.filter(id=id).exists():
            data={
                'success': False,
                'message': 'Product does not exist',
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        product=Product.objects.get(id=id)
        if not Wishlist.objects.filter(product=product,user=user).exists():
            data={
                'success': False,
                'message': 'id is required',
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        try:
            wishlist=Wishlist.objects.get(product=product,user=user)
            wishlist.delete()
            data={
                'success': True,
                'message': 'success',
            }
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            data={
                'success': False,
                'message': str(e),
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
