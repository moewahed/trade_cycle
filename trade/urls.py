from django.urls import path
from .views import index, new_item, request_item, request_status

app_name = 'trade'

urlpatterns = [
    path('', index, name='trade_home'),
    path('add/', new_item, name='new_item'),
    path('request/<int:pk>', request_item, name='request_item'),
    path('request-status/<int:pk>', request_status, name='request_status'),
]
