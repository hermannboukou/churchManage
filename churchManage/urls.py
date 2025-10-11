from django.contrib import admin
from django.urls import path, include
from .views import dashboard_view, login_view, logout_view, profile , configuration



urlpatterns = [
    path('', dashboard_view, name='dashboard'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('settings/', configuration, name='settings'),



    path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
]
