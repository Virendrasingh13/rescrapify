import uuid
import time
from django.core.mail import send_mail
from rescrapify import settings
from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa


def send_email_token(email, slug):
    try:
        # user = User.objects.filter(slug=slug).first()
        # if user.email == email:
        #     message = f"Click on this link to verify your email\nhttp://127.0.0.1:8000/accounts/verify/{slug}"
        # else:
        link = settings.LINK
        message = f"Click on this link to verify your email\n{link}/accounts/verify/{slug}"
        subject = "Verification Token for RESCRAPIFY"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
        return True
        
    except Exception as e:
        print(e)
        return False
    
def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash

        


def send_Contact_mail(name,email,subject,message,phone_no):
    
    try:
        recipient_email = ['notebyharsh@gmail.com',email] 
        email_message = f'Name: {name}\nEmail: {email}\nPhone: {phone_no}\nMessage: {message}'

        send_mail(
                subject,
                email_message,
                settings.EMAIL_HOST_USER, 
                recipient_email,  
                fail_silently=False,
                
                # reply_to=[email],  # This will set the reply-to address in the email client
            )
        
        return True
    
    except Exception as e:
        print(e)
        return False
    
    
    
def send_password_email(email,forgot_password_token):
    try:
        message = f"To reset password for {email}, Click on this link\nhttp://127.0.0.1:8000/accounts/forgot_password/{forgot_password_token}"
        subject = f"RESCRAPIFY - Reset password for {email}"
        email_from = settings.EMAIL_HOST_USER
        receipent = [email]
        send_mail(subject, message, email_from, receipent)
        return True
        
    except Exception as e:
        print(e)
        return False
    
    
#for invoice 
def save_pdf(params:dict):
    template = get_template('invoice.html')
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = uuid.uuid4()
    
    try:
        with open(str(settings.BASE_DIR)+ f"/static/pdfs/{file_name}.pdf", 'wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
            
            if pdf.err:
                return '', False
    

            return file_name, True
            
    except Exception as e:
        print(e)
        


import openpyxl
from django.db import models
from django.http import HttpResponse
from django.utils.text import slugify

def generate_excel(queryset, fields, model_name):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = f"{slugify(model_name)}_data.xlsx"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Create a workbook and add a worksheet
    workbook = openpyxl.Workbook()
    worksheet = workbook.active

    # Write headers (field names)
    worksheet.append(fields)

    # Write data rows
    for obj in queryset:
        row_data = []
        for field in fields:
            field_value = getattr(obj, field)
            if isinstance(field_value, str):
                row_data.append(field_value)
            elif isinstance(field_value, models.ImageField):
                # For ImageField, append the path of the image
                row_data.append(str(field_value))  # Assuming ImageField stores the path as a string
            else:
                row_data.append(str(field_value))  # Convert non-text fields to string
        worksheet.append(row_data)

    # Save workbook to response
    workbook.save(response)

    return response


def download_as_excel(modeladmin, request, queryset):
    # Get all fields including ImageField
    fields = [field.name for field in queryset.model._meta.fields]
    model_name = queryset.model.__name__  # Get model name
    return generate_excel(queryset, fields, model_name)

download_as_excel.short_description = "Download selected items as Excel"


# utils.py
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
from django.utils.text import slugify

def generate_pdf(queryset, fields, model_name):
    response = HttpResponse(content_type='application/pdf')
    filename = f"{slugify(model_name)}_data.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    # Create PDF title with model name
    title = f"{model_name} Data"

    # Create PDF
    doc = SimpleDocTemplate(response, pagesize=letter)
    doc.title = title  # Set PDF title
    table_data = [fields] + [[getattr(obj, field) for field in fields] for obj in queryset]
    table = Table(table_data)

    # Add styling if needed
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)

    # Add table to the PDF
    doc.build([table])

    return response

def download_as_pdf(modeladmin, request, queryset):
    fields = [field.name for field in queryset.model._meta.fields]
    model_name = queryset.model.__name__  # Get model name
    return generate_pdf(queryset, fields, model_name)

download_as_pdf.short_description = "Download selected items as PDF"