"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from users.views import home
from django.conf import settings
from django.conf.urls.static import static
from panel.views import DashboardFuncView

urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("users/", include("users.urls")),
    path("pets/", include("pets.urls")),
    path("painel-admin/", include("panel.urls")),
    path("painel-funcionario/", DashboardFuncView.as_view(), name='painel_funcionario'),
    path("painel-veterinario/", include("consultas.urls")),
    path("produtos/", include("produtos.urls")),
]
 # servir arquivos de mídia em modo de desenvolvimento
if settings.DEBUG:

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
