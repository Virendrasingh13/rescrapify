from django.contrib import admin
from .models import Item, Category, Item_image
from helpers import download_as_pdf

class ItemImageInline(admin.StackedInline):
    model = Item_image
    extra = 1
    actions = [download_as_pdf]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_type')
    prepopulated_fields = {'slug': ('category_name',)}
    actions = [download_as_pdf]

@admin.register(Item_image)
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ('item', 'image_tag')
    actions = [download_as_pdf]

    

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'category_name', 'price', 'seller', 'sold', 'added_at', 'display_first_image')
    list_filter = ('category_name', 'sold', 'added_at')
    search_fields = ('item_name', 'seller__email')
    prepopulated_fields = {'slug': ('item_name',)}
    inlines = [ItemImageInline]
    actions = [download_as_pdf]

   
    def display_first_image(self, obj):
        first_image = obj.item_image.first()
        if first_image:
            return first_image.image_tag()
        return None

    display_first_image.allow_tags = True
    display_first_image.short_description = 'First Image'



