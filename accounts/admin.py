from django.contrib import admin
from .models import CustomUser,Cart,CartItems
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(CartItems)
admin.site.register(Cart)