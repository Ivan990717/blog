"""
URL configuration for djangoProject project.

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
from django.urls import path,re_path
from django.views.static import serve
from myblog import views
from djangoProject.settings import MEDIA_ROOT

urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/',views.login),
    path('get_validCode_img/',views.get_vaildCode_img),
    path('index/',views.index),
    path('logout/',views.log_out),
    re_path('^$',views.index), # 默认首页是index
    path('register/',views.register),
    #media配置
    re_path(r"media/(?P<path>.*)$",serve,{"document_root":MEDIA_ROOT}),

    # 配置个人站点
    re_path('^(?P<username>\w+)$',views.home_site), # 个人主页
    # views.home_site(request,username)
    # re_path('^(?P<username>\w+)/tag/.*/$',views.home_site),
    # re_path('^(?P<username>\w+)/category/.*/$',views.home_site),
    # re_path('^(?P<username>\w+)/archive/.*/$',views.home_site)
    re_path('^(?P<username>\w+)/articles/(?P<article_id>\d+)$',views.article_detail),
    re_path('^(?P<username>\w+)/(?P<condition>tag|category|archive)/(?P<param>.*)/$',views.home_site)
    # views.home_site(request,username,condition = "category",params = "****")
    ]
