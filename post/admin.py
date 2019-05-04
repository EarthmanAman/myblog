from django.contrib import admin

from . models import (
    Category,
    Contact,
    Post,
    SubCategory
)

admin.site.register(Category)
admin.site.register(Contact)
# admin.site.register(Post)
admin.site.register(SubCategory)
