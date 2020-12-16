from django.contrib import admin

from .models import *
from .models import Author, Category, Post
from tinymce.widgets import TinyMCE

class BlogAdmin(admin.ModelAdmin):
    formfield_overides = {
        models.TextField : {'widget': TinyMCE()},
    }

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, BlogAdmin)

