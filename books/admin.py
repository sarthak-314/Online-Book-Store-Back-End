from django.contrib import admin
from .models import Book, BookAD, BookOrder, UserProfile, Blog

admin.site.register(Book)
admin.site.register(BookAD)
admin.site.register(BookOrder)
admin.site.register(UserProfile)
admin.site.register(Blog)