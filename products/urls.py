from django.urls import path
from .views import sellProduct,get_categories_by_type

app_name = 'products'

urlpatterns = [
    path('sellproduct/',sellProduct,name='sell_product'),
    path('get_categories_by_type/', get_categories_by_type, name='get_categories_by_type'),
]   
