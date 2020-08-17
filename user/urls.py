from django.urls import path
from django.conf.urls.static import static
from config import settings
from .views import index, LOGIN, REGISTER, LOGOUT, profile, activate, avatar_change, cover_change

app_name = 'user'

urlpatterns = [
    path('', index, name='home_page'),
    path('<int:pk>/', profile, name='profile_page'),
    path('login/', LOGIN, name='login_page'),
    path('register/', REGISTER, name='register_page'),

    # Function URLs
    path('logout/', LOGOUT, name='logout_function'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('avatar_change', avatar_change, name='avatar_change'),
    path('cover_change', cover_change, name='cover_change'),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
