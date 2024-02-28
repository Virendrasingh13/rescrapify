from django.db import models
from accounts.models import CustomUser
from helpers import generate_unique_hash
# Create your models here.

CATEGORY_CHOICES = [
    ("scrapify","Scrapify"),
    ("creative","Creative"),
]

class Category(models.Model):
    category_name = models.CharField(max_length=50)
    category_choice = models.CharField(choices = CATEGORY_CHOICES, max_length = 10)
    slug = models.SlugField(unique=True, null=True, blank=True)
    
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Category, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.category_name
    
class Item(models.Model):
    item_name = models.CharField(max_length=50)
    category_name = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, default= 0.00)
    description = models.TextField()
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    seller = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

        
    def save(self,*args, **kwargs):
        if not self.slug:
            self.slug = generate_unique_hash()
        super(Item, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.item_name