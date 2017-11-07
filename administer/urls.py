from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^administer$', views.administer, name='administer'),
    url(r'^adminlogin$', views.adminlogin, name='adminlogin'),
    url(r'^adminlogout$', views.adminlogout, name='adminlogout'),
    url(r'^adminhome$', views.adminhome, name='adminhome'),
    url(r'^admingrievance$', views.admingrievance, name='admingrievance'),
    url(r'^admingrievance/(?P<pk>\d+)/$', views.delete, name='delete1234'),
    url(r'^adminsuggestion$', views.adminsuggestion, name='adminsuggestion'),
    url(r'^adminsuggestion/(?P<pk>\d+)/$', views.deletesuggestion, name='deletesuggestion'),
    url(r'^adminelections$', views.adminelections, name='adminelections'),
    url(r'^adminelectionss/(?P<pk>\d+)/$', views.deleteelection, name='deleteelection'),
    url(r'^adminelecresults/(?P<pk>\d+)/$', views.elecresults, name='elecresults'),
    url(r'^addelection', views.addelection, name='addelection'),
    url(r'^adminpolls', views.adminpolls, name='adminpolls'),
    url(r'^deletepolls/(?P<pk>\d+)/$', views.deletepolls, name='deletepolls'),
    url(r'^adminpollresults/(?P<pk>\d+)/$', views.pollresults, name='pollresults'),
    url(r'^addpolls$', views.addpolls, name='addpolls'),
    url(r'^addoptions/(?P<pk>\d+)/$', views.addoptions, name='addoptions'),
    url(r'^addnews$', views.addnews, name='addnews'),
    url(r'^deletenews/(?P<pk>\d+)/$', views.deletenews, name='deletenews'),
    url(r'^candidates/(?P<pk>\d+)/$', views.candidates, name='candidates'),
]