from django.contrib import admin
from django.urls import path, include
from encryption_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', views.signup, name='signup'),
    path('', views.home, name='home'),
    path('profile/', views.profile_view, name='profile'),
    path('audit-logs/', views.audit_logs_view, name='audit_logs'),
]

# Static matrum Media files setup
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
