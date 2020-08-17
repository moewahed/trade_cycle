from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('user.urls')),
    path('blog/', include('blog.urls')),
    path('trade/', include('trade.urls')),
    path('admin/', admin.site.urls),
]
