from django.conf.urls import include, url
from . import views



urlpatterns = [
   url(r'^addTool$', views.addToolView),
   url(r'^deleteTool$', views.deleteToolView),
   url(r'^viewTool$', views.toolProfileView),
   url(r'^tools$', views.listToolsView),
]
