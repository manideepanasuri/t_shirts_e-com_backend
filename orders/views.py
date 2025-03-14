import uuid

from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.models import CartItem, ShippingAddress, Order, OrderItem, OrderPayment
from orders.serializers import CartItemSerializer, ShippingAddressSerializer, OrderSerializer
from store.models import ProductVariation, Wishlist


# Create your views here.

class CartView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        try:
            cart_items=user.cart_items.all()
            cart_items_data=CartItemSerializer(cart_items,many=True).data
            total_cart_price=0
            for x in cart_items_data:
                total_cart_price+=int(x['productVariation']['price'])*int(x['quantity'])

            data={
                'success':True,
                'message':'success',
                'cart_items':cart_items_data,
                'total_cart_price':total_cart_price
            }
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            data={'success':False,
                  'message':str(e)}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

    def post(self,request):
        user = request.user
        product_variation_id=request.data.get('product_variation_id')
        if not ProductVariation.objects.filter(id=product_variation_id).exists():
            data={'success':False,
                  'message':'product_variation_id does not exist'}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

        product_variation=ProductVariation.objects.get(id=product_variation_id)
        if CartItem.objects.filter(productVariation=product_variation,user=user).exists():
            data={'success':False,
                  'message':'product is already in Cart'}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        try:
            quantity=request.data.get('quantity',1)
            if quantity<1:
                data={'success':False,
                      'message':'quantity must be greater than 0'}
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
            cart=CartItem.objects.create(user=user,productVariation=product_variation,quantity=quantity)
            data={'success':True,
                  'message':'success',}
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            data={'success':False,
                  'message':str(e)}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)


    def delete(self,request):
        user = request.user
        product_variation_id=request.data.get('product_variation_id')
        if not ProductVariation.objects.filter(id=product_variation_id).exists():
            data={'success':False,
                  'message':'product_variation_id does not exist'}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        product_variation=ProductVariation.objects.get(id=product_variation_id)
        if not CartItem.objects.filter(productVariation=product_variation,user=user).exists():
            data={'success':False,
                  'message':'product_variation_id does not exist'}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        try:
            cart_item=CartItem.objects.get(productVariation=product_variation,user=user)
            cart_item.delete()
            data={'success':True,
                  'message':'success',}
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            data={'success':False,
                  'message':str(e)}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
    def put(self,request):
        user = request.user
        product_variation_id=request.data.get('product_variation_id')
        quantity=request.data.get('quantity',1)
        if quantity<1:
            data={'success':False,
                  'message':'quantity must be greater than 0'}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        if not ProductVariation.objects.filter(id=product_variation_id).exists():
            data={'success':False,
                  'message':'product_variation_id does not exist'}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        product_variation=ProductVariation.objects.get(id=product_variation_id)
        if not CartItem.objects.filter(productVariation=product_variation,user=user).exists():
            data={'success':False,
                  'message':'cartitem does not exist'}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)
        try:
            cart_item=CartItem.objects.get(productVariation=product_variation,user=user)
            cart_item.quantity=quantity
            cart_item.save()
            data={'success':True,
                  'message':'success',}
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            data={'success':False,
                  'message':str(e)}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)





class ShippingAddressView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        full_name=request.data.get('full_name')
        address_line_1=request.data.get('address_line_1')
        address_line_2=request.data.get('address_line_2')
        city=request.data.get('city')
        state=request.data.get('state')
        pin_code=request.data.get('pin_code')
        phone_number=request.data.get('phone_number')
        email=request.data.get('email')
        try:
            shipping_address=ShippingAddress.objects.create(
                user=user,
                full_name=full_name,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                state=state,
                pin_code=pin_code,
                phone_number=phone_number,
                email=email
            )
            order=Order.objects.create(user=user,address=shipping_address,total_amount=0)
            cartitems=user.cart_items.all()
            total_payment=0
            for cart in cartitems.all():
                if cart.productVariation.price is None:
                    cartprice=cart.productVariation.product.price
                else:
                    cartprice=cart.productVariation.price
                price=cartprice*cart.quantity
                total_payment+=price
                OrderItem.objects.create(order=order,product_variation=cart.productVariation,quantity=cart.quantity,price=price)
            order.total_amount=total_payment
            order.save()
            order_payment=OrderPayment.objects.create(order=order,amount=total_payment,transaction_id=str(uuid.uuid4()))

            data={'success':True,
                  'message':'success'}
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            data={'success':False,
                  'message':str(e)}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

    def get(self,request):
        user = request.user
        try:
            if not ShippingAddress.objects.filter(user=user).exists():
                data={'success':False,
                      'message':'Shipping Address does not exist'}
                return Response(data,status=status.HTTP_400_BAD_REQUEST)
            shipping_address=ShippingAddress.objects.get(user=user)
            data={'success':True,
                  'message':'success',
                  'shipping_address':ShippingAddressSerializer(shipping_address).data}
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            data={'success':False,
                  'message':str(e)}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

    def put(self,request):
        user = request.user
        try:
            shipping_address=ShippingAddress.objects.get(user=user)
            shipping_address.full_name=request.data.get('full_name')
            shipping_address.address_line_1=request.data.get('address_line_1')
            shipping_address.address_line_2=request.data.get('address_line_2')
            shipping_address.city=request.data.get('city')
            shipping_address.state=request.data.get('state')
            shipping_address.pin_code=request.data.get('pin_code')
            shipping_address.phone_number=request.data.get('phone_number')
            shipping_address.email=request.data.get('email')
            shipping_address.save()
            data={'success':True,
                  'message':'success',
                  'shipping_address':ShippingAddressSerializer(shipping_address).data}
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            data={'success':False,
                  'message':str(e)}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        user = request.user
        try:
            shipping_address=ShippingAddress.objects.get(user=user)
            shipping_address.delete()
            data={'success':True,
                  'message':'success'}
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            data={'success':False,
                  'message':str(e)}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)

class OrdersView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = request.user
        try:
            orders=user.orders.all().order_by('-id')
            data={'success':True,
                  'message':'success',
                  'data':OrderSerializer(orders,many=True).data
                  }
            return Response(data,status=status.HTTP_200_OK)
        except Exception as e:
            data={'success':False,
                  'message':str(e)}
            return Response(data,status=status.HTTP_400_BAD_REQUEST)