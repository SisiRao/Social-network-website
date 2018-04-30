from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

	url(r'^$', views.index, name='index'),
    url(r'^profile/(?P<user_id>\d+)$', views.profile, name='profile'),
    url(r'^filter$',views.filter,name='filter'),
    url(r'^newpost$', views.newpost, name='newpost'),
    url(r'^newclothes/(?P<id>\d+)$', views.newclothes, name='newclothes'),
    url(r'^photo/(?P<id>\d+)$', views.get_photo, name='photo'),
    url(r'^clothes_photo/(?P<id>\d+)$', views.get_clothes_photo, name='clothes_photo'),
    url(r'^delete/(?P<id>\d+)$', views.delete, name='delete'),
    url(r'^forgetPassword$', views.forgetPassword, name='forgetPassword'),
    url(r'^edit_profile$', views.edit_profile, name='edit_profile'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name': 'OOTD/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    url(r'^register$', views.register, name='register'),
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9]+)/(?P<token>[a-z0-9\-]+)$',
        views.confirm_registration, name='confirm'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^getclothes/(?P<id>\d+)$', views.getclothes, name='getclothes'),
    url(r'^product$', views.product, name='product'),

    url(r'^reset_password_email$', views.reset_password_email, name="reset_password_email"),
    url(r'^reset_password/(?P<username>\w+)$', views.reset_password, name="reset_password"),

    url(r'^follow/(?P<user_id>\d+)$', views.follow, name='follow'),
    url(r'^unfollow/(?P<user_id>\d+)$', views.unfollow, name='unfollow'),
    url(r'^location$', views.location, name='location'),
    url(r'^get_picture/(?P<id>\d+)$', views.get_picture, name='get_picture'),
    url(r'^relocate$', views.relocate, name='relocate'),

    url(r'^like/(?P<id>\d+)$', views.like, name='like'),
    url(r'^unlike/(?P<id>\d+)$', views.unlike, name='unlike'),
    url(r'^get-list-json/(?P<max_pk>.+)$', views.getchanges)


]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
