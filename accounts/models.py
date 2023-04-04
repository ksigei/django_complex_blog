from django.db import models

from django.contrib.auth.models import User

from django.urls import reverse

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='images/avatars', blank=True)
    cover_image = models.ImageField(upload_to='images/cover_images', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('profile_detail', args=[str(self.id)])
    
    class Meta:
        verbose_name_plural = 'Profiles'
