from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, login_view, logout_view

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
        success_url='/accounts/login/'
    ), name='password_change'),
]
