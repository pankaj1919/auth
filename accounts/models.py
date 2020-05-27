from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    phone=models.CharField(max_length=100,null=True,blank=True)
    image=models.ImageField(null=True,blank=True)
    gender=models.CharField(max_length=100,null=True,blank=True)
    position=models.CharField(max_length=100,null=True,blank=True)
    email_confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Profile"

    def __str__(self):
        return f'{self.user.username} Profile'


    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url