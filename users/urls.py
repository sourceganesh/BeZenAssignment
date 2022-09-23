from django.urls import path
from .views import edit_profile, login_view, logout_page, register_user, view_profile

app_name = 'users'

urlpatterns = [
    path('login/', login_view, name="login"),
    path('register/', register_user, name="register"),
    path('logout/', logout_page, name="logout"),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('view_profile/<str:username>/', view_profile, name='view_profile'),
] 