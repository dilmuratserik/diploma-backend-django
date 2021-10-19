from django.db import models

class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    
