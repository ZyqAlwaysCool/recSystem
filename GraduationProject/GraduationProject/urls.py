"""GraduationProject URL Configuration

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
from django.contrib import admin
from Spark import views as spark_views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^zyq/', spark_views.zyq),
    url(r'^getUsrRecMsg/', spark_views.getUserRecMsg, name='getUserRecMsg'),
    url(r'^getItemRecMsg/', spark_views.getItemRecMsg, name='getItemRecMsg'),
    url(r'^rateTheMovie/', spark_views.rateTheMovie, name='rateTheMovie'),
    url(r'^getHistoricalData/', spark_views.getHistoricalData, name='getHistoricalData'),
    url(r'^detail/', spark_views.getFullMovieInfo, name='getFullMovieInfo'),
    url(r'^login/', spark_views.login, name='login'),
    url(r'^register/', spark_views.register, name='register'),
    url(r'^all/', spark_views.allMovie, name='all'),
    url(r'^records/', spark_views.records, name='records'),
    url(r'^favor/', spark_views.favor, name='favor'),
    url(r'^rank/', spark_views.rank, name='rank'),
    url(r'^index/', spark_views.home, name='home'),
    url(r'^allmovies/', spark_views.all_movies, name='allmovies'),
    url(r'^ranklist/', spark_views.rank_list, name='ranklist'),
    url(r'^single/', spark_views.single_movie_detail, name='single'),
]
