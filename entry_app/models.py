from django.db import models


# Create your models here.
class Visitor(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=264)
    phone = models.CharField(max_length=15, unique=True)
    check_in = models.DateTimeField(auto_now_add=True)
    hostname = models.CharField(max_length=128)
    check_out = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.name + " " + self.email


class Host(models.Model):
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=264)
    phone = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name + " " + self.email
