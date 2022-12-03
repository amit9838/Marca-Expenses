from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserPreferences(models.Model):
    user  = models.OneToOneField(to=User,on_delete=models.CASCADE )
    currency = models.CharField(max_length=225, blank=True, null=True, default=None)

    def __str__(self):
        return str(self.user)+"'s " + 'prefreferences'
    
    class Meta:
        verbose_name_plural = 'User Preferences'

