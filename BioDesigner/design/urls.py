from django.conf.urls import patterns, include, url
from django.contrib import admin
from design import views

urlpatterns = patterns('',
    url(r'^search$', views.searchParts),
    url(r'^get$', views.getParts),
    url(r'^dashboard$', views.dashboardView),
    url(r'^updateChain$', views.saveChain),
    url(r'^newProject$', views.createProject),
    url(r'^getChain$', views.getProjectChain)
)
