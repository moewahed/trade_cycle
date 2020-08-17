from django.urls import path
from .views import blog_info, new_blog, new_comment

app_name = 'blog'

urlpatterns = [
    path('<int:pk>/', blog_info, name='blog_details'),
    path('new/', new_blog, name='new_blog'),
    path('comment/<int:pk>', new_comment, name='new_comment'),
]
