from django.contrib import admin
from .models import BlogImage, CommentImage, ItemImage, ReviewImage

admin.site.register(BlogImage)
admin.site.register(CommentImage)
admin.site.register(ItemImage)
admin.site.register(ReviewImage)
