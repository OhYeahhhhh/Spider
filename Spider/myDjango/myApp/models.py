from django.db import models

# Create your models here.
class Weathers(models.Model):
    wCity = models.CharField(max_length=20)
    wDate = models.CharField(max_length=20)
    wWeather = models.CharField(max_length=20)
    wTemp = models.CharField(max_length=20)

class Movies(models.Model):
    mid= models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    score=models.CharField(max_length=20)

class Phones(models.Model):
    pNo = models.CharField(max_length=7)
    pBrand = models.CharField(max_length=100)
    pPrice = models.CharField(max_length=20)
    pContent = models.CharField(max_length=100)
    pFile = models.CharField(max_length=20)

class Packages(models.Model):
    pPrice = models.CharField(max_length=7)
    pTitle = models.CharField(max_length=100)