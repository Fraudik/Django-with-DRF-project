"""
URL configuration for config project.

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
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView

admin.site.site_header = "Longevity In Time"
admin.site.index_title = 'Admin page'

urlpatterns = [
    path("docs/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema")),

    path('users/', include('users.urls')),
    path('products/', include('products.urls')),
    path('search/', include('search.urls')),
    path('chat/', include('chats.urls')),
    path('api/v2/', include('config.routers')),

    path('admin/', admin.site.urls),
]
