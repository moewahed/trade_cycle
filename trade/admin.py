from django.contrib import admin
from .models import Item, Review, Request, Notification


admin.site.register(Item)
admin.site.register(Review)
admin.site.register(Request)
admin.site.register(Notification)
