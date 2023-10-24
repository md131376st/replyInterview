from django.contrib import admin
from django.contrib.auth.models import User

from bookshelf.models import Book

# Register your models here.
admin.site.register( Book )
