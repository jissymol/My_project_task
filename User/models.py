from datetime import date

from django.db import models


# Create your models here.

class Registration(models.Model):
    username=models.CharField(max_length=200)
    firstname=models.CharField(max_length=200)
    lastname=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    photo=models.ImageField(upload_to='book_media')
    contact=models.IntegerField()
    password1=models.CharField(max_length=200)
    password2=models.CharField(max_length=200)

    def __str__(self):
        return str(self.username)

class Logintable(models.Model):
    username = models.CharField(max_length=200)
    password1 = models.CharField(max_length=200)
    password2 = models.CharField(max_length=200)
    type=models.CharField(max_length=200)

    def __str__(self):
        return str(self.username)



class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1000)
    userid=models.ForeignKey(Registration,on_delete=models.CASCADE)
    blog_images=models.ImageField(upload_to='book_media')
    Date = models.DateField(default=date.today)

    def __str__(self):
        return str(self.title)

class Comment(models.Model):
    comment = models.CharField(max_length=500)
    email=models.CharField(max_length=200)
    userid = models.ForeignKey(Registration, on_delete=models.CASCADE)
    blogid=models.ForeignKey(Blog,on_delete=models.CASCADE,null=True, blank=True)
    Date = models.DateField(default=date.today)

    def __str__(self):
        return str(self.comment)
