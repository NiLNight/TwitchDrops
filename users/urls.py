from django.urls import path
# from .views import UserRegistration, UserDetail, UserList, UserDelete, UserDeleteAll
from .views import UserRegistration

app_name = 'users'

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='user-register'),
#     path('user/<slug:slug>/', UserDetail.as_view(), name='user-detail'),
#     path('users/', UserList.as_view(), name='user-list'),
#     path('delete/<slug:slug>/', UserDelete.as_view(), name='user-delete'),
]