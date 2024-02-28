from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from accounts.models import CustomUser
from django.contrib.auth import get_user_model,login,logout,authenticate
from django.views.decorators.csrf import csrf_exempt
from helpers import send_email_token
import json
from django.contrib import messages
from helpers import generate_unique_hash

# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from .serializers import MyTokenObtainPairSerializer
# from rest_framework.response import Response

User = get_user_model()

# Create your views here.
def LoginView(request):
    
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect('home:home')
    else:
        if request.method == "POST":
            try:
                # body = request.data
                body = request.POST
                print(body)
                if ('email' in body and 'password' in body):
                    email = body['email']
                    password = body['password']
                    
                    user_obj = User.objects.filter(email=email).first()
                    
                    if user_obj and not user_obj.is_superuser:
                        if not user_obj.is_verified:
                            raise Exception('You have to verify your mail through link sent to you by mail')
                        
                        user = authenticate(request=request, email=email, password=password)
                        if user:
                            login(request=request,user=user)
                            return redirect('home:home')
                            # print(login(request=request,user=user))
                            # refresh = MyTokenObtainPairSerializer.get_token(user=user)
                            # return Response({
                            #     # 'refresh': str(refresh),
                            #     # 'access': str(refresh.access_token),
                            #     'success':True,
                            #     'message':'Login Success'
                            # })
                        else:
                            raise Exception('Invalid Password!')
                    else:
                        raise Exception("No user with this email exists!")
                    
                else:
                    raise Exception('Provide proper credentials to login')
                    
            except Exception as e:
                messages.warning(request, str(e))
                return HttpResponseRedirect(request.path_info)
                # return JsonResponse({'success':False, 'message':str(e)})
            
        
        return render(request, 'accounts/login.html')
   

def Register(request):
    
    if request.user.is_authenticated:
        messages.success(request, "You are already logged in")
        return redirect('home:home')
    
    else:  
        if request.method == "POST":
            try:
                body = request.POST
                # body = request.data
                if ('email' in body and 'password' in body):
                    email = body['email']
                    password = body['password']
                    first_name = body['first_name']
                    phone_no = body['phone_no']
                    last_name = body['last_name']
                    user_image = request.FILES.get('user_image')
                    if user_image: 
                        if user_image.size > 1*1024*1024:
                            raise Exception('Image size should be less than 1MB')
                    
                    user, created = User.objects.get_or_create(email=email)
                    if created :
                        user.first_name = first_name
                        user.phone_no = phone_no
                        user.last_name = last_name
                        user.set_password(password)
                        user.user_image = user_image
                        
                        user.save()
                        email_sent = send_email_token(email, user.slug)
                        if email_sent: 
                            messages.success(request, "Verification mail is sent your email")
                            return HttpResponseRedirect(request.path_info)
                            # return JsonResponse({
                            #     'success':True,
                            #     'message':'Verification mail is sent your email'
                            # })
                        else:
                            raise Exception('There is some problem in sending mail')
                            # return JsonResponse({
                            #     'success':False,
                            #     'message':"There's some problem in sending mail"
                            # })
                        
                    else:
                        raise Exception('User with this email already exists')
                    
                else:
                    raise Exception('Provide proper credentials ')
            
            except Exception as e:
                messages.warning(request, str(e))
                return HttpResponseRedirect(request.path_info)
                # return JsonResponse({
                #     'status':False,
                #     'message':str(e)
                #     })
                
        return render(request, 'accounts/signup.html')

def verify(request, slug):
    try:
        user = User.objects.filter(slug=slug).first()
        if user:
            if user.is_verified :
                if user.temp_email != None:
                    user.email = user.temp_email
                    user.temp_email = None
                    user.save()
                    logout(request)
                    context = {
                        'success': True,
                        'message': 'New email set Successfully'
                    }
                    context_obj = { 'data':json.dumps(context)}
                    return render(request, 'accounts/verify.html', context_obj) 
                    
                context = {
                    'success': True,
                    'message': 'Your email is already verified. Youc can login'
                }
            
            user.is_verified = True
            user.save()
            context = {
                    'success': True,
                    'message': 'Your email is verified. You can login'
                }
        
        else:
            raise Exception('Invalid verification link!')
        
    except Exception as e:
        print(e)
        context = {
                    'success': False,
                    'message': str(e)
                }
    finally:
        context_json = json.dumps(context)
        context_obj = { 'data':context_json}
        return render(request, 'accounts/verify.html', context_obj) 
        

def LogoutView(request):
    logout(request)
    return redirect('accounts:login')



def editProfile(request):
    if request.user.is_authenticated:
        
        if request.method == "POST":
            try:
                body = request.POST
                print(body)
                if 'first_name' in body and 'last_name' in body and 'email' in body and 'phone_no' in body:
                    user = request.user
                    if user.email == body['email']:
                        
                        user.first_name = body['first_name']
                        user.phone_no = body['phone_no']
                        user.last_name = body['last_name']
                        user.city = body['city']
                        user.state = body['state']
                        user_image = request.FILES.get('user_image')
                        if user_image: 
                            if user_image.size > 1*1024*1024:
                                raise Exception('Image size should be less than 1MB')
                            else:
                                user.user_image = user_image
                            
                        user.save() 
                        messages.success(request, "Profile updated successfully")
                        return HttpResponseRedirect(request.path_info)
                    else:
                        raise Exception('Do not try anything funny with email here')
                else:
                    raise Exception('Provide your all details to complete profile')
                    
            except Exception as e:
                messages.success(request, str(e))
                return HttpResponseRedirect(request.path_info)
            
        if request.method == "GET":
            # print(request.user.user_image.url)
            return render(request, 'accounts/edit_profile.html')
        
    else:
        messages.warning(request,'You must be logged in to access this page.')
        return redirect('accounts:login')
            
    
def change_password(request):
    
    if request.method == "POST":
        try:
            body = request.POST
            if 'cur_password' in body and 'new_password' in body:
                cur_password = body['cur_password']
                new_password = body['new_password']
                
                user = authenticate(request, email=request.user.email, password=cur_password)   
                if user:
                    user.set_password(new_password)
                    user.save()
                    # messages.success(request, 'Password changed successfully, You have to login again')
                    return JsonResponse({'success':True, 'message':'Password changed successfully, You have to login again'})
                
                else:
                    raise Exception('Invalid password!')    
                
            else:
                raise Exception('Insufficient credentials')   
                  
        except Exception as e:
            print(e)
            # messages.warning(request, str(e))
            return JsonResponse({'success':False,'message':str(e)})
    else:
        return redirect('accounts:edit_profile')
            
            
def change_email(request):
    if request.method == "POST":
       try:
            body = request.POST
            print(body)
            if 'cur_email' in body and 'new_email' in body:
                cur_email = body['cur_email']
                new_email = body['new_email']
                
                if cur_email == request.user.email:
                    user = User.objects.filter(email=cur_email).first()
                    
                    user.slug = generate_unique_hash()
                    user.temp_email = new_email
                    user.save()
                    email_sent = send_email_token(new_email, user.slug)
                    if email_sent:
                        return JsonResponse({'success':True, 'message':'Verification is sent on your new email'})
                    else:
                        raise Exception('There is some problem in sending mail')
                    
                else:
                    raise Exception('Invalid current email!')
            else:
                raise Exception('Insufficient credentials!')
       except Exception as e:
           print(e)
           return JsonResponse({'success':False,'message':str(e)})
       
    else:
        return redirect('accounts:edit_profile')
       
        