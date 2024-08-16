"""
URL configuration for PocketDungSite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings #добалвяем 
from django.conf.urls.static import static #добалвяем 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')), #добавляем путь для ckeditor
    path('wiki/', include('wiki.urls')),
    path('', include('visitka.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #добавляем 

#if settings.DEBUG: #добавляем 
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #добавляем
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #добавляем 