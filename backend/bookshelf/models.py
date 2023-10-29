from django.contrib.auth.models import User
from django.db import models
from djmoney.models.fields import MoneyField


# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Book(models.Model):
    id = models.BigAutoField(primary_key=True)
    authors = models.ManyToManyField(Author, related_name="book_list", blank=True)
    title = models.CharField(max_length=30, unique=True)
    year = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # price = MoneyField(max_digits=10, decimal_places=2, null=True, default_currency='EUR')

    def __str__(self):
        return self.title


class Review(models.Model):
    id = models.BigAutoField(primary_key=True)
    review = models.TextField()
    book = models.ForeignKey( Book,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rate = models.IntegerField()

    def __str__(self):
        return self.book.title + " " + self.user.username + " "+ self.review +" " +self.rate