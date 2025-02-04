from django.contrib import admin
from library.models import Account, Book, BookRequest
# Register your models here.
admin.site.register(Account)
admin.site.register(Book)
admin.site.register(BookRequest)
