from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^$', views.all_events_view, name='eventos'),
    url(r'^(?P<pk>[0-9]+)/$', views.event_view, name='evento'),
    url(r'^criar/$', views.create_event, name='criar'),
    url(r'^criar_sucesso/$', views.create_success, name='criar_sucesso'),
    url(r'^gerir_eventos/$', views.manage_events, name='gerir'),
    url(r'^gerir_evento/(?P<pk>[0-9]+)/$', views.manage_events_view, name='gerir_view'),
    url(r'^validar/(?P<pk>[0-9]+)/$', views.validate_event, name='validar'),
    url(r'^editar/(?P<pk>[0-9]+)/$', views.edit_event, name='editar'),
    url(r'^remover/(?P<pk>[0-9]+)/$', views.remove_event, name='remover'),
    ]
