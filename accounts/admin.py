from django.contrib import admin
from .models import CustomUser, Cart, CartItems, LikedProducts, order

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'phone_no', 'is_verified')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_verified',)

admin.site.register(CustomUser, CustomUserAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_paid')
    list_filter = ('is_paid',)
    readonly_fields = ('get_cart_total',)

admin.site.register(Cart, CartAdmin)

class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('cart', 'item', 'get_item_price')

admin.site.register(CartItems, CartItemsAdmin)

class LikedProductsAdmin(admin.ModelAdmin):
    list_display = ('user', 'item')

admin.site.register(LikedProducts, LikedProductsAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'created_at', 'amount')
    search_fields = ('order_id', 'user__email', 'bill_name')
    list_filter = ('created_at',)
    readonly_fields = ('name',)

admin.site.register(order, OrderAdmin)
