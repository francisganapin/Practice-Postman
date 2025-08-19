from django.db import models

class Brand(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class Phone(models.Model):
    brand = models.ForeignKey(Brand,related_name='phones',on_delete=models.CASCADE)
    model_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    stock = models.PositiveBigIntegerField(default=0)


    def __str__(self):
        return f"{self.brand.name} - {self.model_name}"