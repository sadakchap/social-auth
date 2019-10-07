from django.conf import settings
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='home'),
    path('about/',views.about,name='about'),
    path('accounts/',include('accounts.urls')),
    path('images/',include('images.urls')),
    path('',include('django.contrib.auth.urls')),
    path('oauth/',include('social_django.urls',namespace='social')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
