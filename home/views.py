from django.http import JsonResponse,HttpResponseRedirect
from django.shortcuts import render
from rest_framework.views import APIView
from helpers import send_Contact_mail
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    
    if request.method == "POST":
        try:
            if request.user.is_authenticated:
                # body = request.data
                body = request.POST
                print(body)
                if ('name' in body and 'email' in body and 'phone_no' in body and 'subject' in body) :
                    if request.user.email == body['email']:
                        name = body['name']
                        email = body['email']
                        phone_no = body['phone_no']
                        subject = body['subject']
                        message = body['message']
                        
                        email_sent = send_Contact_mail(name,email,subject,message,phone_no)
                        if email_sent:
                            messages.success(request, "Email is sent")
                            return HttpResponseRedirect(request.path_info)
                        # return JsonResponse({
                            #     'success':True,
                            #     'message':'Email is sent'
                            # })
                        else:
                            raise Exception('Can not send the mail ')
                        
                    else:
                        raise Exception('Use the same email you logged in with.')
                        
                else:
                    raise Exception('Provide proper credentials')   
            else:
                raise Exception("You need to be logged in to send mail")
        except Exception as e:
            messages.warning(request, str(e))
            return HttpResponseRedirect(request.path_info)
            # return JsonResponse({'success':False, 'message':str(e)})
        
    return render(request,'contact.html')
    
    
    
    