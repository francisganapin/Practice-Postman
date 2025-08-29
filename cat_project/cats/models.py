from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name
    
class Cat(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='cats')

    def __str__(self):
        return self.name