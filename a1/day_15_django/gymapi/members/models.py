from django.db import models

# Create your models here.

class Member(models.Model):
    name = models.CharField(max_length=100)
    membership_type = models.CharField(max_length=50)
    join_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name