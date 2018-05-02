from django.contrib import admin
from blog.models import Post, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ['id','title','count_text']
    list_display_links = ['title']

    def count_text(self,post):
        return '{}글자'.format(len(post.text))
    count_text.short_description = '내용 글자수'

admin.site.register(Post,PostAdmin)
admin.site.register(Comment)