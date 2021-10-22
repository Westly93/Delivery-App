from django.db import models
from django_resized import ResizedImageField


class MenuItem(models.Model):
    name= models.CharField(max_length= 50)
    description= models.TextField()
    image= ResizedImageField(size= [200, 200], quality= 100, upload_to= 'Menu Images')
    price= models.DecimalField(max_digits= 5, decimal_places= 2)
    category= models.ManyToManyField('Category', blank= True, related_name= 'item')

    def __str__(self):
        return self.name



class Category(models.Model):
    name= models.CharField(max_length= 100)


    def __str__(self):
        return self.name

class OrderModel(models.Model):
    created_on= models.DateTimeField(auto_now_add= True)
    price= models.DecimalField(max_digits= 7, decimal_places= 2)
    items= models.ManyToManyField('MenuItem', related_name= 'order', blank= True)
    name= models.CharField(max_length= 50, blank= True)
    email= models.EmailField(blank= True)
    street= models.CharField(max_length= 50, blank= True)
    city= models.CharField(max_length= 50, blank= True)
    state= models.CharField(max_length= 15, blank= True)
    zip_code= models.IntegerField(null= True, blank= True)
    is_paid= models.BooleanField(default= False)
    is_shipped= models.BooleanField(default= False)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'

