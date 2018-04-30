from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'^$', views.globalstream, name='home'),
    url(r'^globalstream$', views.globalstream, name='globalstream'),
    url(r'^followerstream/(?P<user_id>\d+)$', views.followerstream, name='followerstream'),
    url(r'^register$', views.register, name='register'),
    # Route for built-in authentication with our own custom login page
    url(r'^login$', auth_views.login, {'template_name':'socialnetwork/login.html'}, name='login'),
    # Route to logout a user and send them back to the login page
    url(r'^logout$', auth_views.logout_then_login, name='logout'),
    # The following URL should match any username valid in Django and
    # any token produced by the default_token_generator
    url(r'^confirm-registration/(?P<username>[a-zA-Z0-9]+)/(?P<token>[a-z0-9\-]+)$',
        views.confirm_registration, name='confirm'),

    url(r'^profile/(?P<user_id>\d+)$', views.profile, name='profile'),
    url(r'^edit_profile$', views.edit_profile, name='edit_profile'),
    url(r'^follow/(?P<user_id>\d+)$', views.follow, name='follow'),
    url(r'^unfollow/(?P<user_id>\d+)$', views.unfollow, name='unfollow'),
    url(r'^new_post$', views.new_post, name='new_post'),
    url(r'^get_picture/(?P<id>\d+)$', views.get_picture, name='get_picture'),

    url(r'^get-posts-json$', views.get_posts_json, name='get_posts_json'),
    url(r'^get-posts-follow-json/(?P<user_id>\d+)$', views.get_posts_follow_json, name='get_posts_follow_json'),
    url(r'^get-comments-json$', views.get_comments_json, name='get_comments_json'),
    url(r'^add-comment/(?P<post_id>\d+)$', views.add_comment, name='add_comment')
]