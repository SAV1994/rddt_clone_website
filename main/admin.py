from django.contrib import admin

from .models import Pt, AdvUser, Comment, Comment_to_comment

class  PtAdmin (admin.ModelAdmin):
	list_display = ('title', 'author', 'content', 'created_at', 'image', 'is_active')
	list_display_links = ('author', 'title', 'is_active')
	search_fields = ('author', 'title', 'is_active',)

class  CommentAdmin (admin.ModelAdmin):
	list_display = ('author', 'content', 'created_at','is_active')
	list_display_links = ('author', 'is_active')
	search_fields = ('author', 'is_active',)

class  Comment_to_commentAdmin (admin.ModelAdmin):
	list_display = ('author', 'content', 'created_at','is_active')
	list_display_links = ('author', 'is_active')
	search_fields = ('author', 'is_active',)

admin.site.register(Pt, PtAdmin) 
admin.site.register(AdvUser) 
admin.site.register(Comment, CommentAdmin)
admin.site.register(Comment_to_comment, Comment_to_commentAdmin)