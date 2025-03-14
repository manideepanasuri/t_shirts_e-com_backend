from django.contrib import admin

from orders.models import *

# Register your models here.
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    can_delete = False
    verbose_name_plural = 'Order Items'
    verbose_name = 'Order Item'
    fields = ('product', 'quantity', 'price')
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user','status','total_amount','created_at')
    filter=('status','created_at')
    inlines = (OrderItemInline,)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(OrderPayment)
admin.site.register(CartItem)
