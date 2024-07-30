from django.contrib import admin
from .models import Post,Author,Tag,Comment
# Register your models here.
class Postadmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}
    list_display = ('title', 'author')
    list_filter = ('tags','author','date')
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_name','post',)
admin.site.register(Post,Postadmin)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment,CommentAdmin)
