# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.apps import apps

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.core import serializers

from OOTD.models import *
from OOTD.forms import *
from django.db import transaction
# Used to generate a one-time-use token to verify a user's email address
from django.contrib.auth.tokens import default_token_generator
# Used to send mail from within Django
from django.core.mail import send_mail
from OOTD.forms import *
from OOTD.models import *
import json
from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext



@login_required
def chat(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")

    # Render that in the index template
    return render(request, "OOTD/chat.html", {
        "rooms": rooms,
    })


@login_required
def index(request):
    outfits = Outfit.objects.filter(Q(publicity = 'PU') | Q(created_by = request.user)).order_by('-likes' ,'-creation_time')
    clothes = Clothes.objects.all()

    profile_item = Profile.objects.get(user=request.user)
    liked_outfits = profile_item.liked_outfit.all()

    form = filterForm()
    context = {'outfits':outfits, 'clothes':clothes, 'form' :form, 'profile' :profile_item, "liked_outfits":liked_outfits}

    return render(request, 'OOTD/index.html', context)

@login_required
def getchanges(request,max_pk):
    outfits = Outfit.objects.filter(id__gt=max_pk).distinct().order_by("creation_time")

    response_text = serializers.serialize('json', outfits, use_natural_foreign_keys = True)
    # print response_text;
    return HttpResponse(response_text, content_type='application/json')



@login_required
@transaction.atomic
def like(request,id):
    curr_outfit = Outfit.objects.get(id=id)
    profile_item = Profile.objects.get(user=request.user)
    profile_item.liked_outfit.add(curr_outfit);
    profile_item.save();
    # print (len(list(profile_item.liked_outfit.all())))

    curr_outfit.favorite_by.add(request.user)
    curr_outfit.likes = curr_outfit.likes + 1
    curr_outfit.save();

    return HttpResponse('', content_type='application/json')


@login_required
@transaction.atomic
def unlike(request,id):
    outfit = Outfit.objects.get(id=id)
    outfit.favorite_by.remove(request.user)
    outfit.likes = outfit.likes - 1
    outfit.save();
    profile_item = Profile.objects.get(user=request.user)
    profile_item.liked_outfit.remove(outfit);
    profile_item.save();

    print (len(list(profile_item.liked_outfit.all())))

    return HttpResponse('', content_type='application/json')


def forgetPassword(request):
    return render(request, 'OOTD/forgetPassword.html')


@login_required
def filter(request):
    if (request.method == "GET"):
        form = filterForm()
        outfits = Outfit.objects.all().order_by("-creation_time")
        clothes = Clothes.objects.all()
        context = {'outfits':outfits, 'clothes':clothes, 'form' :form}
        return render(request, 'OOTD/index.html',  context)

    if(request.method == "POST"):
        outfitslist = Outfit.objects.all()
        clotheslist = Clothes.objects.all()
        form = filterForm()

        # if request.POST.get("height") and request.POST.get("height") != "":
        #     height = request.POST['height']
        #     outfitslist1 = Outfit.objects.filter(height = height)
        #     outfitslist = list(outfitslist1)

        if request.POST.get("season") and request.POST.get("season") != "":
             season = request.POST['season']
             outfitslist2 = Outfit.objects.filter(season = season)
             outfitslist2 = list(outfitslist2)
             outfitslist  = list(set(outfitslist2).intersection(set(outfitslist)))

        if request.POST.get("gender") and request.POST.get("gender") != "":
            gender = request.POST['gender']
            outfitslist3 = Outfit.objects.filter(gender = gender)
            outfitslist3 = list(outfitslist3)
            outfitslist  = list(set(outfitslist).intersection(set(outfitslist3)))

        if request.POST.get("size") and request.POST.get("size") != "":
            size = request.POST['size']
            print(size)
            clotheslist1 = Clothes.objects.filter(size = size)
            outfitslist4 = []
            for clothes in clotheslist1:
                outfitslist4.append(clothes.outfit)
            outfitslist = list(set(outfitslist).intersection(set(outfitslist4)))

        if request.POST.get("brand") and request.POST.get("brand") != "":
            brand = request.POST['brand']
            print(brand)
            clotheslist2 = Clothes.objects.filter(brand = brand)
            outfitslist5 = []
            for clothes in clotheslist2:
                outfitslist5.append(clothes.outfit)
            outfitslist = list(set(outfitslist).intersection(set(outfitslist5)))

        if request.POST.get("color") and request.POST.get("color") != "":
            color = request.POST['color']
            print(color)
            clotheslist3 = Clothes.objects.filter(color = color)
            outfitslist6 = []
            for clothes in clotheslist3:
                outfitslist6.append(clothes.outfit)
            outfitslist = list(set(outfitslist).intersection(set(outfitslist6)))

        # search for keyword
        if request.POST.get("searchword") and request.POST.get("searchword") != "":
            searchword = request.POST['searchword']
            allclothes = Clothes.objects.filter(Q(description__contains = searchword) | Q(labelName__contains = searchword) | Q(detail__contains = searchword))
            outfits1 = Outfit.objects.filter(description__contains = searchword)

            outfits1 = list(outfits1)
            outfit2 = []
            for clothes in allclothes:
                outfit2.append(clothes.outfit)

            in_first = set(outfits1)
            in_second = set(outfit2)
            in_second_but_not_in_first = in_second - in_first
            outfitslist7 = outfits1 + list(in_second_but_not_in_first)
            outfitslist = list(set(outfitslist).intersection(set(outfitslist7)))

        clotheslist = Clothes.objects.filter(outfit__in = outfitslist)

        context = {'outfits':outfitslist, 'clothes':clotheslist, 'form' :form}
        return render(request, 'OOTD/index.html',  context)


@login_required
def profile(request, user_id):

    # If the user is trying to access his/her own profile, redirect to edit_profile
    if int(user_id) == int(request.user.id):
        outfit = Outfit.objects.all()
        print(request.user)
        outfitslist1 = Outfit.objects.filter(created_by = request.user)
        outfitslist1 = list(outfitslist1)
        outfitslist2 = Outfit.objects.filter(favorite_by = request.user)
        outfitslist2 = list(outfitslist2)
        clotheslist1 = Clothes.objects.filter(outfit__in = outfitslist1)
        clotheslist2 = Clothes.objects.filter(outfit__in = outfitslist2)
        profile_item = Profile.objects.get(user=request.user)
        follow_list = Profile.objects.get(user=request.user).follow_list.all()
        followed_by = Profile.objects.get(user=request.user).followed_by.all()
        liked_outfits = profile_item.liked_outfit.all()
        context = {'profile': profile_item, 
               'follow_list': follow_list, 
               'form': EditProfileForm(), 
               'follow_number': len(follow_list), 
               'followed_number': len(followed_by),
               'outfits1':outfitslist1,
               'outfits2':outfitslist2,
               'clothes1':clotheslist1,
               'clothes2':clotheslist2,
               'liked_outfits':liked_outfits,
               }
        return render(request, 'OOTD/profile1.html', context)
    

    viewed_user = User.objects.get(id=user_id)
    if viewed_user in request.user.profile.follow_list.all():
        is_followed = True
    else:
        is_followed = False

    #get the outfit posted by the user
    outfit = Outfit.objects.all()
    print(viewed_user)
    outfits1 = Outfit.objects.filter(created_by = viewed_user)
    outfits1 = list(outfits1)
    outfits2 = Outfit.objects.filter(favorite_by = viewed_user)
    outfits2 = list(outfits2)
    clothes1 = Clothes.objects.filter(outfit__in = outfits1)
    clothes2 = Clothes.objects.filter(outfit__in = outfits2)
    print(outfits1)

    profile_item = Profile.objects.get(user__id=user_id)
    liked_outfits = profile_item.liked_outfit.all()
    follow_list = Profile.objects.get(user=viewed_user).follow_list.all()
    followed_by = Profile.objects.get(user=viewed_user).followed_by.all()

    context = {'profile': profile_item, 
               'follow_list': follow_list, 
               'followed_by': followed_by,
               'is_followed':is_followed,
               'follow_number': len(follow_list), 
               'followed_number': len(followed_by),
               'outfits1':outfits1,
               'outfits2':outfits2,
               'clothes1':clothes1,
               'clothes2':clothes2,
               'liked_outfits':liked_outfits,
               }
    return render(request, 'OOTD/profile1.html', context)



@login_required
@transaction.atomic
def newpost(request):
    if request.method == 'GET':
        newPost = Outfit(
            created_by=request.user
        )
        form = outfitForm(instance=newPost)
        context = {'form': form}
        return render(request, 'OOTD/newpost.html', context)

    context = {}

    newOutfit = Outfit(
        created_by=request.user, creation_time=timezone.now(), last_changed=timezone.now(),
        description=request.POST['description'], gender=request.POST['gender'],
        height=request.POST['height'], likes=0, season=request.POST['season'], publicity=request.POST['publicity']
    )
    form = outfitForm(request.POST, request.FILES, instance=newOutfit)
    form.save()
    # print(Outfit.objects.all())
    context['outfit'] = newOutfit
    # context['form'] = form
    newClothes = Clothes(owned_by=request.user)
    clothesform = clothesForm(instance=newClothes)
    context['clothesform'] = clothesform
    return render(request, 'OOTD/new_clothes.html', context)


@login_required
@transaction.atomic
def newclothes(request, id):
    # if request.method == 'GET':
    #     newClothes = Clothes(owned_by=request.user)
    #     form = clothesForm(instance=newClothes)
    #     context={'form':form}
    #     return render(request, 'OOTD/new_clothes.html', context)

    outfit = Outfit.objects.get(id=id)

    newClothes = Clothes(
        owned_by=request.user,
        gender=request.POST['gender'], color=request.POST['color'], category=request.POST['category'],
        price=request.POST['price'], size=request.POST['size'],
        brand=request.POST['brand'],
        url=request.POST['url'], description=request.POST['description'], outfit=outfit,
        top=request.POST['mapper_top'], left = request.POST['mapper_left']
    )

    # newClothes.save()
    clothesform = clothesForm(request.POST, request.FILES, instance=newClothes)
    clothesform.save()
    context = {'clothes': newClothes, 'clothesform': clothesform, 'outfit': outfit}
    return render(request, 'OOTD/new_clothes.html', context)


@login_required
def get_photo(request, id):
    item = get_object_or_404(Outfit, id=id)
    if not item.picture:
        raise Http404
    return HttpResponse(item.picture)

@login_required
def get_clothes_photo(request, id):
    item = get_object_or_404(Clothes, id=id)
    if not item.picture:
        raise Http404
    return HttpResponse(item.picture)


def contact(request):
    if request.method == 'GET':
        return render(request, 'OOTD/contact.html')
    userName=request.user.username
    email_body = """
	User {user} sent you an email, here is the message:
	{message}
	and user's email: {email}
	""".format(user=request.user,
               message=request.POST['message'],
               email=request.user.email)

    send_mail(subject="Message from customer "+userName,
              message=email_body,
              from_email="ootdteamandrew@gmail.com",
              recipient_list=["ootdteamandrew@gmail.com"])
    context={}
    context['success'] = "Your email has been successfully sent! We will contact you soon!"
    return render(request, 'OOTD/contact.html', context)


@login_required
def product(request):
    return render(request, 'OOTD/product.html')


@login_required
def getclothes(request, id):
    item = get_object_or_404(Clothes, id = id)
    context = {"clothes":item}
    return render(request, 'OOTD/product.html',context)

@login_required
@transaction.atomic
def delete(request, id):
    deleted = Outfit.objects.get(id=id)
    deletedClothes = Clothes.objects.filter(outfit=deleted)
    for deletedCloth in deletedClothes:
        deletedCloth.picture.delete(save=True)

    deleted.picture.delete(save=True)
    deleted.delete()
    return redirect(reverse('index'))

@transaction.atomic
def register(request):
    context = {}
    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'OOTD/register.html', context)

    # Creates a bound form from the request POST parameters and makes the
    # form available in the request context dictionary.
    form = RegistrationForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'OOTD/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'],
                                        password=form.cleaned_data['password1'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.is_active = False
    new_user.save()


    new_profile = Profile( user = new_user,
						   first_name = form.cleaned_data['first_name'],
						   last_name  = form.cleaned_data['last_name'],
						   email      = form.cleaned_data['email'],
	                       height     = 0,
	                       gender     = "Not specified",
	                       bio        = "Hello Outfit of the day!",
                           occupation = "Designer",
                           longitude = form.cleaned_data['longitude'],
                           latitude = form.cleaned_data['latitude']
                           )

    new_profile.save()

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
              from_email="ootdteamandrew@gmail.com",
              recipient_list=[new_user.email])

    context['email'] = form.cleaned_data['email']

    return render(request, 'OOTD/needs-confirmation.html', context)


@transaction.atomic
def confirm_registration(request, username, token):
    user = get_object_or_404(User, username=username)

    # Send 404 error if token is invalid
    if not default_token_generator.check_token(user, token):
        raise Http404

    # Otherwise token was valid, activate the user.
    user.is_active = True
    user.save()

    return render(request, 'OOTD/confirmed.html', {})


def reset_password_email(request):
    context = {}

    try:
        print(request)
        print(request.GET['email'])
        user = User.objects.get(email=request.GET['email'])
        print(user)

    except ObjectDoesNotExist:
        context['message'] = "Email not found, please enter your registered email."
        return render(request, "OOTD/forgetpassword.html", context)

    email_body = """
		Please click following link to reset your passwrod.
		 \n http://%s%s""" % (request.get_host(), reverse('reset_password', args=(user.username,)))

    send_mail(subject="Password change link",
              message=email_body,
              from_email="ootdteamandrew@gmail.com",
              recipient_list=[user.email]),

    # message = "We have sent a link to the email you registered. " \
    #           "Please follow the instrument and reset your password."
    context['email'] = user.email

    return render(request, 'OOTD/need_resetpwd.html', context)

@transaction.atomic
def reset_password(request, username):
    if request.method == "GET":
        form = PasswordEditForm_forget()
        context = {'form': form}
        context['username'] = username

        return render(request, 'OOTD/reset_password.html', context)

    form = PasswordEditForm_forget(request.POST)

    if not form.is_valid():
        form = PasswordEditForm_forget()
        context = {'form': form}  # existing entry.
        context["message"] = "passwords did not match."

        return render(request, 'OOTD/reset_password.html', context)

    try:
        user_User = User.objects.get(username__exact=username)
        # user_Users = Profile.objects.filter(user=user_User)


    except Profile.DoesNotExist:
        print(testing3)
        form = PasswordEditForm_forget()
        context = {'form': form}  # existing entry.
        context["message"] = "Unexpected Error, Please re-fill your password."
        context['username'] = username

        return render(request, 'OOTD/reset_password.html', context)

    except User.DoesNotExist:
        print(testing2)
        form = PasswordEditForm_forget()
        context = {'form': form}  # existing entry.
        context["message"] = "Unexpected Error, Please re-fill your password."
        context['username'] = username

        return render(request, 'OOTD/reset_password.html', context)

    # user_Users.update(password=form.cleaned_data['password'])
    user_User.set_password(form.cleaned_data['password'])
    user_User.save()
    new_user = authenticate(username=user_User.username, password=form.cleaned_data['password'])

    login(request, new_user)
    print("testing")

    return index(request)


@transaction.atomic
@login_required
def follow(request, user_id):
    errors = []
    viewed_user = User.objects.get(id=user_id)
    if request.method == 'POST':
        f_list = request.user.profile.follow_list
        f_list.add(User.objects.get(id=user_id))
        f_by = viewed_user.profile.followed_by
        f_by.add(User.objects.get(id=request.user.id))
        is_followed = True
    else:
        errors.append('Follow must use POST method')
        is_followed = False

    profile_item = get_object_or_404(Profile, user__id=user_id)
    follow_list = Profile.objects.get(user=viewed_user).follow_list.all()
    followed_by = Profile.objects.get(user=viewed_user).followed_by.all()
    context = {'profile': profile_item, 'follow_list': follow_list, 'followed_by': followed_by, 'is_followed':is_followed,
               'form': EditProfileForm(), 'follow_number': len(follow_list), 'followed_number': len(followed_by)}
    return render(request, 'OOTD/profile1.html', context)


@transaction.atomic
@login_required
def unfollow(request, user_id):
    errors = []
    viewed_user = User.objects.get(id=user_id)
    if request.method == 'POST':
        f_list = request.user.profile.follow_list
        f_list.remove(User.objects.get(id=user_id))
        f_by = viewed_user.profile.followed_by
        f_by.remove(User.objects.get(id=request.user.id))
        is_followed = False
    else:
        errors.append('Unfollow must use POST method')
        is_followed = True

    profile_item = get_object_or_404(Profile, user__id=user_id)
    follow_list = Profile.objects.get(user=viewed_user).follow_list.all()
    followed_by = Profile.objects.get(user=viewed_user).followed_by.all()
    context = {'profile': profile_item, 'follow_list': follow_list, 'followed_by': followed_by,'is_followed':is_followed,
               'form': EditProfileForm(), 'follow_number': len(follow_list), 'followed_number': len(followed_by)}
    return render(request, 'OOTD/profile1.html', context)

@login_required
@transaction.atomic
def relocate(request):
    errors = []
    message = ''
    if not request.method == 'POST':
        errors.append('Edit profile should use POST method')
        profile_item = Profile.objects.get(user=request.user)
        follow_list = Profile.objects.get(user=request.user).follow_list.all()
        followed_by = Profile.objects.get(user=request.user).followed_by.all()
        context = {'profile': profile_item, 'follow_list': follow_list, 'followed_by':followed_by,
                   'form': EditProfileForm(), 'follow_number': len(follow_list),'followed_number': len(followed_by)}
        return render(request, 'OOTD/profile1.html', context)
    new_profile = Profile.objects.get(user=request.user)
    # If user choose to update location
    if request.POST['longitude'] != "" and request.POST['latitude'] != "":
        new_profile.longitude = request.POST['longitude']
        new_profile.latitude = request.POST['latitude']
        new_profile.save()
    else:
        errors.append('Could not locate you')

    profile_item = Profile.objects.get(user=request.user)
    follow_list = Profile.objects.get(user=request.user).follow_list.all()
    followed_by = Profile.objects.get(user=request.user).followed_by.all()
    context = {'profile': profile_item, 'follow_list': follow_list, 'followed_by': followed_by,
               'form': EditProfileForm(), 'follow_number': len(follow_list), 'followed_number': len(followed_by)}

    return render(request, 'OOTD/profile1.html', context)

@login_required
@transaction.atomic
def edit_profile(request):
    errors = []
    message = ''
    if not request.method == 'POST':
        errors.append('Edit profile should use POST method')
        profile_item = Profile.objects.get(user=request.user)
        follow_list = Profile.objects.get(user=request.user).follow_list.all()
        context = {'profile': profile_item, 'errors': errors, 'followlist': follow_list, 'form': EditProfileForm(), 'follow_number': len(follow_list)}
        return render(request, 'OOTD/profile1.html', context)

    new_profile = Profile.objects.get(user=request.user)
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
        if request.POST['occupation']:
            new_profile.occupation = request.POST['occupation']
            new_profile.save()
        if request.POST['bio']:
            new_profile.bio = request.POST['bio']
            new_profile.save()
        else:
            errors.append('Please enter your bio')

    profile_item = Profile.objects.get(user=request.user)
    follow_list = Profile.objects.get(user=request.user).follow_list.all()
    context = {'message': message, 'profile': profile_item, 'errors': errors, 'followlist': follow_list,
               'form': EditProfileForm(), 'follow_number': len(follow_list)}

    return render(request, 'OOTD/profile1.html', context)


@login_required
def get_picture(request, id):
    profile_item = get_object_or_404(Profile, user__id=id)
    return HttpResponse(profile_item.picture, content_type='image')


@login_required
def get_photo(request,id):
    outfit = get_object_or_404(Outfit, id=id)
    return HttpResponse(outfit.picture, content_type='image')


def location(request):
    lc = []
    for profile in Profile.objects.all():
        dic = {"pk": profile.id, "geometry": {"type": "Point", "coordinates": [profile.longitude, profile.latitude]}}
        lc.append(dic)

    result = {"features": lc}

    response_text = json.dumps(result)
    return HttpResponse(response_text, content_type='application/json')


def handler404(request):
    response = render_to_response('404.html', {},
                              context_instance=RequestContext(request))
    response.status_code = 404
    return response

@login_required
def topic(request):
    return render(request, 'OOTD/topic.html')

