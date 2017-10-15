"""profiles_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from profiles_api import templates

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('profiles_api.urls')),
    url(r'^login/', templates.login),
    url(r'^logout/', templates.logout),
    url(r'^register/', templates.register),
    url(r'^dashboard/', templates.dashboard),
    url(r'^create_event/', templates.create_event),
    url(r'^places/', templates.places),
    url(r'^people/', templates.people),
    url(r'^activities/', templates.activities),
    url(r'^$', templates.dashboard),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
