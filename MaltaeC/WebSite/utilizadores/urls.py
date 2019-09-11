from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^registo', views.register),
	url(r'^login$' , views.loginView),
	url(r'^loginForm$' , views.loginFormView),
	url(r'^logout$' , views.logoutView),
	url(r'^perfil$' , views.viewProfile),
	url(r'^editProfile$' , views.edit_profile),
	url(r'^editProfile#(?P<default>\w+?)$' , views.edit_profile),
	url(r'^editProfileAction$' , views.edit_profile_action),
	url(r'^uploadImageAction$' , views.upload_image_view),
	url(r'^resetPassword$' , views.resetPasswordInsertView),
	url(r'^resetPasswordConfirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)$' , views.resetPasswordConfirmView, name='resetPasswordConfirm'),
	url(r'^delete5Image$' , views.delete_5Image),
	url(r'^artesaos$' , views.verTodosArtesaosCriativos),
	url(r'^upload5ImageAction$' , views.upload_5Image),
	url(r'^chageUserVideo$' , views.change_user_video),
]
