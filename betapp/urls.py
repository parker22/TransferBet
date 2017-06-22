from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^updateOdds/$', views.updateOdds, name='updateOdds'),
    url(r'^latestBetOdds/$', views.odds_detail),
    url(r'^latestClubsRumors/$', views.rumors_detail ),

]