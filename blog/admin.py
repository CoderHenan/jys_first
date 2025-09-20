from django.contrib import admin
from .models import *
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','content','pubt_time','category','author']
    list_filter = ['title','pubt_time','category','author']
    fields = ['title','content','category','author']



class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']


class BlogCommentAdmin(admin.ModelAdmin):
    list_display = ['content','pub_time','author','blog']


admin.site.register(BlogCategory,BlogCategoryAdmin)
admin.site.register(Blog,BlogAdmin)
admin.site.register(BlogComment,BlogCommentAdmin)