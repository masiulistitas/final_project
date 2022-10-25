from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', args=[str(self.id)])


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name='notes')
    image = models.ImageField(upload_to="images", default='default.png', blank=True)
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        if not self.image:
            self.image = 'default.png'
        super(Note, self).save(*args, **kwargs)
