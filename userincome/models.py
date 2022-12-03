from tabnanny import verbose
from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
class UserIncome(models.Model):
    amount = models.FloatField()
    date = models.DateField(default = now)
    description = models.TextField()
    owner = models.ForeignKey(to = User, on_delete= models.CASCADE)
    source = models.CharField(max_length=256)

    def __str__(self):
        return self.source

    class Meta:
        ordering = ['-date']

class Source(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name