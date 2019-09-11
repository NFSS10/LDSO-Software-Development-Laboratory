from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^manage', views.manage),
	url(r'^aprovarUser', views.aprovarUser),
	url(r'^reprovarUser', views.reprovarUser),
	url(r'^banirUser', views.banirUser),
	url(r'^desbanirUser', views.desbanirUser),
	url(r'^criarEntrevista', views.criarEntrevista),
	url(r'^adicionarEntrevista', views.addEntrevista),
	url(r'^reprovados', views.validarReprovado),
	url(r'^mudarCarousel', views.mudarCarousel),
	url(r'^addAdmin', views.registarAdmin),
	url(r'^allUsers', views.verTodosUsers),


]
