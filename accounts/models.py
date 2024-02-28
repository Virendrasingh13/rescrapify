from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from helpers import generate_unique_hash
from django.core.validators import MaxValueValidator,MinValueValidator

# Create your models here.

class CustomUser(AbstractUser):
    username = models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, verbose_name='username',null=True, blank=True)
    email = models.EmailField(unique=True,max_length = 255)
    slug = models.SlugField(unique=True, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    user_image = models.ImageField(upload_to = 'images/user/',null=True, blank=True)
    phone_no = models.IntegerField(validators=[MaxValueValidator(999999999999),MinValueValidator(000000000000)],null=True, blank=True,default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    state = models.CharField(max_length=100,null=True, blank=True,default=None)
    city = models.CharField(max_length=150,null=True, blank=True,default=None)
    temp_email = models.EmailField(null=True,blank=True,max_length = 255,default= None)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def name(self):
        return self.first_name +" "+ self.last_name
    
    def __str__(self) -> str:
        return self.email
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(CustomUser, self).save(*args, **kwargs)
            
    
    