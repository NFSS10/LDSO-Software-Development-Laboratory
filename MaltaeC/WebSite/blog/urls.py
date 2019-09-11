from django.conf.urls import url
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^$', views.blog_view, name='blog'),
	url(r'^register_post', views.register_post, name="register_post"),
    url(r'^add_post', views.add_post, name='add_post'),
    url(r'^delete_post/(?P<id>[0-9]+)/$', views.delete_post, name='delete_post'),
    url(r'^save_post/(?P<id>[0-9]+)/$', views.save_post, name="save_post"),
    url(r'^edit_post/(?P<id>[0-9]+)/$', views.edit_post, name='edit_post')
    ]
