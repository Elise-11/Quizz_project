"""Quizz_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.views.generic.base import TemplateView

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from Quizz_project_app.views import register, login_user, choice, logoutUser, explo, QuizzMicro,microscopy_correction
from Quizz_project_app.views import QuizzCompo, component_correction, autocompletion, exploResults
from django.conf import settings

from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login_user, name='login'),
    path('register/', register, name='register'),
    path('logout/', logoutUser, name='logout'),
    path('choice/', choice, name='choice'),
    path('QuizzCompo/', QuizzCompo.as_view(), name='QuizzCompo'),
    path('QuizzMicro/', QuizzMicro.as_view(), name='QuizzMicro'),
    path('QuizzMicro/Correction', microscopy_correction, name='microscopy_correction'),
    path('QuizzCompo/Correction', component_correction, name='component_correction'),
    path('explo/', explo, name='explo'),
    path('Results/', exploResults, name='exploResults'),
    path('autocompletion/', autocompletion, name="autocompletion"),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns