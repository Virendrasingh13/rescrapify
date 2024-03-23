from django.contrib import admin
from .models import CustomUser, Cart, CartItems, LikedProducts, order
from helpers import download_as_excel,download_as_pdf

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'phone_no', 'is_verified', 'image_tag', 'created_at', 'updated_at', 'state', 'city',)
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_no', 'state', 'city')
    list_filter = ('is_verified', 'created_at', 'updated_at')
    actions = [download_as_excel,download_as_pdf]

admin.site.register(CustomUser, CustomUserAdmin)


class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_paid')
    list_filter = ('is_paid',)
    readonly_fields = ('get_cart_total',)
    actions = [download_as_excel,download_as_pdf]

admin.site.register(Cart, CartAdmin)

class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('cart', 'item', 'get_item_price')
    actions = [download_as_excel,download_as_pdf]

admin.site.register(CartItems, CartItemsAdmin)

class LikedProductsAdmin(admin.ModelAdmin):
    list_display = ('user', 'item')
    actions = [download_as_excel,download_as_pdf]

admin.site.register(LikedProducts, LikedProductsAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'created_at', 'amount')
    search_fields = ('order_id', 'user__email', 'bill_name')
    list_filter = ('created_at',)
    readonly_fields = ('name',)
    actions = [download_as_excel,download_as_pdf]

admin.site.register(order, OrderAdmin)



