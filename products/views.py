from django.http import JsonResponse
from django.shortcuts import render,redirect
from .models import Category,Item
from django.contrib import messages

# Create your views here.
def sellProduct(request):
    
    if request.user.is_authenticated:
    
        if request.method == "POST":
            try:
                body = request.POST
                print(body)
                if 'category_slug' in body and 'item_name' in body and 'price' in body and 'item_image' in request.FILES  and 'description' in body:
                    item_name = body['item_name']
                    category_slug = body['category_slug']
                    price = body['price']
                    item_image = request.FILES.get('item_image')
                    description = body['description']
                    user = request.user
                    print(user)
                    if item_image.size > 1*1024*1024:
                            raise Exception('Image size should be less than 1MB')
                        
                    category_obj = Category.objects.filter(slug=category_slug).first()
                    item_obj,created = Item.objects.get_or_create(item_name= item_name, seller=user, price=price,category_name=category_obj)
                    if created:
                        item_obj.description = description
                        item_obj.image = item_image
                        
                        item_obj.save()
                        messages.success(request,'Product added for sell successfully.')
                        return redirect('products:sell_product')
                        
                    else:
                        raise Exception('You have already added one product with same details')
                    
                else:
                    raise Exception('Insuffiecient ditails provided')
            except Exception as e:
                print(e)
                messages.warning(request,str(e))
                return redirect('products:sell_product')
    
        category = Category.objects.all()
        return render(request,'products/sell_product.html',{'category':category})
    
    else:
        messages.warning(request,'You must be logged in to access this page.')
        return redirect('accounts:login')


def get_categories_by_type(request):
    try:
        if request.method == "GET" and 'type' in request.GET:
            category_type = request.GET['type']
            categories_obj = Category.objects.filter(category_type=category_type)
            if categories_obj:
                categories = [{'category_name':category.category_name, 'slug':category.slug } for category in categories_obj]
                return JsonResponse({'success':True,'categories':categories})
            else:
                raise Exception("Don't try anything funny with the fields")
        else :
            raise Exception('Invalid category request')
    except Exception as e:
        print(e)
        return JsonResponse({'success':False,'message':str(e)})
        