"""iot_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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

from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.front , name = 'front'),
    path('home/', views.index , name = 'index'),
    path('front/', views.front , name = 'front'),
    path('topuser/', views.topuser , name = 'topuser'),
    path('livemembers/', views.livemembers , name = 'livemembers'),
    path('editdata/', views.editdata , name = 'editdata'),
    path('hkshkjbsdlJBLMB/', views.index1 , name = 'index1'),
    path('process/', views.process, name = 'process'),
    path('analysis/', views.analysis, name='analysis'),
    path('manage/', views.manage , name = 'manage'),
    path('manage1/', views.manage1, name='manage1'),
    path('check/', views.check , name = 'check'),
    path('cardselect/', views.card , name = 'card'),
    path('datafs/', views.datafs , name = 'datafs'),
    path('logsrch/', views.logsrch , name = 'logsrch'),
    path('download_csv/', views.download_csv, name='download_csv'),
    path('cardedit/', views.edit , name = 'cardedit'),
    path('switchuser/', views.switchuser , name = 'switchuser'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('searchuser/', views.search , name = 'search'),
]
