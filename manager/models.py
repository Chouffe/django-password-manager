from django.db import models


# Create your models here.
class Entry(models.Model):
    title = models.CharField(max_length=200)
    comment = models.TextField()
    username = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    expires = models.DateField(null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    password = models.CharField(max_length=200)
