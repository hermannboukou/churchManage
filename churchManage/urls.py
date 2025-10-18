from django.contrib import admin
from django.urls import path, include
from .views import dashboard_view, login_view, logout_view, profile , configuration
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', dashboard_view, name='dashboard'),

   # path('', include('core.urls')),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    path('settings/', configuration, name='settings'),
    path('admin/', admin.site.urls),
    path('meetings/', include('meetings.urls')),
    path('members/', include('members.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
