from django.db import models

# Create your models here.

class Category(models.Model): 
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True) 

    def __str__(self): 
        return self.title