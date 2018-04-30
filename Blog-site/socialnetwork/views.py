from __future__ import unicode_literals
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.core import serializers
from socialnetwork.forms import RegistrationForm, PostForm, EditProfileForm
from socialnetwork.models import Profile, Post, Comment
from django.db import transaction
# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator
# Used to send mail from within Django
from django.core.mail import send_mail
import json


@transaction.atomic
def register(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])

    # Mark the user as inactive to prevent login before email confirmation.
    new_user.is_active = False
    new_user.save()



    # Give every new user a default profile
    default_profile = Profile(
        owner=new_user
    )
    default_profile.save()

    # Generate a one-time use token and an email message body
    token = default_token_generator.make_token(new_user)

    email_body = """
    Please click the link below to verify your email address and
    complete the registration of your account:
      http://{host}{path}
    """.format(host=request.get_host(),
               path=reverse('confirm', args=(new_user.username, token)))

    send_mail(subject="Verify your email address",
              message=email_body,
              from_email="yuzhey@andrew.cmu.edu",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']
    return render(request, 'socialnetwork/needs-confirmation.html', context)


@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()

    return render(request, 'socialnetwork/confirmed.html', {})


@login_required
def globalstream(request):

        globalpost = Post.objects.all().order_by('-post_time')
        context = { 'globalpost':globalpost, 'form': PostForm()}
        return render(request, 'socialnetwork/globalstream.html', context)


@login_required
def followerstream(request, user_id):
    followlist = Profile.objects.get(owner__id=user_id).follow_list.all()
    followerpost = Post.objects.filter(post_by__in=followlist).order_by('-post_time')
    selfpost = Post.objects.filter(post_by=request.user.id)
    context = {'followerpost': followerpost | selfpost, 'form': PostForm()}
    return render(request, 'socialnetwork/followerstream.html', context)


@login_required
def profile(request, user_id):

    # If the user is trying to access his/her own profile, redirect to edit_profile
    if int(user_id) == int(request.user.id):
        profile_item = Profile.objects.get(owner=request.user)
        followlist = Profile.objects.get(owner=request.user).follow_list.all()
        context = {'profile': profile_item, 'followlist': followlist, 'form': EditProfileForm()}
        return render(request, 'socialnetwork/profile.html', context)

    viewed_user = User.objects.get(id=user_id)
    if viewed_user in request.user.profile.follow_list.all():
        is_followed = True
    else:
        is_followed = False
    profile_item = Profile.objects.get(owner__id=user_id)
    context = {'profile': profile_item, 'is_followed': is_followed}
    return render(request, 'socialnetwork/profile.html', context)


@transaction.atomic
@login_required
def edit_profile(request):
    errors = []
    message = ''
    if not request.method == 'POST':
        errors.append('Edit profile should use POST method')
        profile_item = Profile.objects.get(owner=request.user)
        follow_list = Profile.objects.get(owner=request.user).follow_list.all()
        context = {'profile': profile_item, 'errors': errors, 'followlist': follow_list}
        return render(request, 'socialnetwork/profile.html', context)

    new_profile = Profile.objects.get(owner=request.user)
    # If user choose to update both picture and bio
    if request.FILES:
        profile_form = EditProfileForm(request.POST, request.FILES, instance=new_profile)
        if not profile_form.is_valid():
            errors.append('Edition not valid')
        else:
            new_profile.content_type = profile_form.cleaned_data['picture'].content_type
            profile_form.save()
            new_profile.save()
            message = 'Profile edited'
    # If the user just update the bio
    else:
        if request.POST['bio']:
            new_profile.bio = request.POST['bio']
            new_profile.save()
        else:
            errors.append('Please enter your bio')

    profile_item = Profile.objects.get(owner=request.user)
    follow_list = Profile.objects.get(owner=request.user).follow_list.all()
    context = {'message': message, 'profile': profile_item, 'errors': errors, 'followlist': follow_list, 'form': EditProfileForm()}
    return render(request, 'socialnetwork/profile.html', context)


@transaction.atomic
@login_required
def new_post(request):
    errors = []
    if not request.method == 'POST':
        errors.append('New Post should use POST method')
        globalpost = Post.objects.all().order_by('-post_time')
        context = {'errors':errors, 'globalpost': globalpost, 'form': PostForm()}
        return render(request, 'socialnetwork/globalstream.html', context)

    post = Post(post_by=request.user, post_time=timezone.now())
    create_post = PostForm(request.POST, instance=post)
    if not create_post.is_valid():
        errors.append('Post not valid')
        globalpost = Post.objects.all().order_by('-post_time')
        context = {'errors': errors, 'globalpost': globalpost, 'form': PostForm()}
        return render(request, 'socialnetwork/globalstream.html', context)

    create_post.save()
    # message = 'Post created'
    # Show by reverse-chronological order
    # globalpost = Post.objects.all().order_by('-post_time')
    # context = {'message': message, 'globalpost': globalpost, 'form': PostForm()}
    # return render(request, 'socialnetwork/globalstream.html', context)
    return redirect('globalstream')


@login_required
def get_picture(request, id):
    profile_item = get_object_or_404(Profile, owner__id=id)

    return HttpResponse(profile_item.picture, content_type='image')


@transaction.atomic
@login_required
def follow(request, user_id):
    errors = []
    if request.method == 'POST':
        f_list = request.user.profile.follow_list
        f_list.add(User.objects.get(id=user_id))
        is_followed = True
    else:
        errors.append('Follow must use POST method')
        is_followed = False

    profile_item = get_object_or_404(Profile, owner__id=user_id)
    context = {'profile': profile_item, 'errors': errors, 'is_followed': is_followed}
    return render(request, 'socialnetwork/profile.html', context)


@transaction.atomic
@login_required
def unfollow(request, user_id):
    errors = []
    if request.method =='POST':
        f_list = request.user.profile.follow_list
        f_list.remove(User.objects.get(id=user_id))
        is_followed = False
    else:
        errors.append('Unfollow must use POST method')
        is_followed = True

    profile_item = get_object_or_404(Profile, owner__id=user_id)
    context = {'profile': profile_item, 'errors': errors, 'is_followed': is_followed}
    return render(request, 'socialnetwork/profile.html', context)


@transaction.atomic
@login_required
def add_comment(request, post_id):
    if request.method != 'POST':
        raise Http404

    if 'new_comment'not in request.POST or not request.POST['new_comment']:
        message = 'You must enter an comment to post.'
        json_error = '{ "error": "'+message+'" }'
        return HttpResponse(json_error, content_type='application/json')

    new_comment = Comment(comment_content=request.POST['new_comment'], comment_by=User.objects.get(id=request.user.id),
                          comment_time=timezone.now(), post=Post.objects.get(id=post_id))
    new_comment.save()

    response_text = serializers.serialize('json', Comment.objects.filter(post__id=post_id))
    return HttpResponse(response_text, content_type='application/json')


@login_required
def get_posts_json(request):
    #response_text = serializers.serialize('json', Post.objects.filter(post_time__gt=request.GET['latest_post']))
    li = []
    for post in Post.objects.filter(post_time__gt=request.GET['latest_post']):
        dic = {"model": "socialnetwork.post", "pk": post.id,
               "fields": {"post_by_id": post.post_by.id, "post_by": post.post_by.username, "post_content": post.post_content,
                          "post_time": post.post_time.strftime("%Y-%m-%d %H:%M:%S")}}
        li.append(dic)

    response_text = json.dumps(li)
    return HttpResponse(response_text, content_type='application/json')


@login_required
def get_posts_follow_json(request, user_id):
    followlist = Profile.objects.get(owner__id=user_id).follow_list.all()
    followerpost = Post.objects.filter(post_by__in=followlist)
    selfpost = Post.objects.filter(post_by=request.user.id)
    follow_self_post = followerpost | selfpost
    #response_text = serializers.serialize('json', follow_self_post.filter(post_time__gt=request.GET['latest_post_follow']))
    ls = []
    for post in follow_self_post.filter(post_time__gt=request.GET['latest_post_follow']):
        dic = {"model": "socialnetwork.post", "pk": post.id,
               "fields": {"post_by_id": post.post_by.id, "post_by": post.post_by.username, "post_content": post.post_content,
                          "post_time": post.post_time.strftime("%Y-%m-%d %H:%M:%S")}}
        ls.append(dic)

    response_text = json.dumps(ls)
    return HttpResponse(response_text, content_type='application/json')


@login_required
def get_comments_json(request):
    #response_text = serializers.serialize('json', Comment.objects.filter(comment_time__gt=request.GET['latest_comment']))
    lc = []
    for comment in Comment.objects.filter(comment_time__gt=request.GET['latest_comment']):
        dic = {"model": "socialnetwork.comment", "pk": comment.id,
               "fields": {"comment_by_id": comment.comment_by.id, "comment_by": comment.comment_by.username,
                          "post_id": comment.post.id, "comment_content": comment.comment_content,
                          "comment_time": comment.comment_time.strftime("%Y-%m-%d %H:%M:%S")}}
        lc.append(dic)

    response_text = json.dumps(lc)
    return HttpResponse(response_text, content_type='application/json')
