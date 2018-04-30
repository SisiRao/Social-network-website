from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from OOTD.choice import *

# Create your models here.

# Brand Model
# class Brand(models.Model):
#     name = models.CharField(max_length=2, choices=BRAND_CHOICES)
#     favorite_by = models.ManyToManyField(User, related_name="brand_favorite_by", blank=True, null=True)

# Tag Model
class Tag(models.Model):
    name = models.CharField(max_length=20)


# New Post Model
class Outfit(models.Model):
    created_by = models.ForeignKey(User, related_name="outfit_created_by")
    creation_time = models.DateTimeField()
    last_changed = models.DateTimeField()
    description = models.CharField(max_length=200)
    picture = models.FileField(upload_to="images/outfit")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    height = models.CharField(max_length=3, choices=HEIGHT_CHOICES)
    season = models.CharField(max_length=1, choices=SEASON_CHOICES)
    publicity = models.CharField(max_length=2, choices=PUBLICITY_CHOICES)
    favorite_by = models.ManyToManyField(User, related_name="outfit_favorite_by")
    likes = models.IntegerField(blank=True,default=0)


class Brand(models.Model):
    name = models.CharField(max_length=50)
    favorite_by = models.ManyToManyField(User, related_name="brand_favorite_by")


# Clothes Model
class Clothes(models.Model):
    picture = models.FileField(upload_to="images/clothes")
    description = models.CharField(max_length=200, blank=True, null=True)
    owned_by = models.ForeignKey(User, related_name="clothes_owned_by")
    brand = models.CharField(max_length=2, choices=BRAND_CHOICES)
    color = models.CharField(max_length=1, choices=COLOR_CHOICES)
    price = models.CharField(max_length=4, choices=PRICE_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    labelName = models.CharField(max_length=20)
    url = models.CharField(max_length=200, blank=True, default='')
    category = models.CharField(max_length=2, choices=CATEGORY_CHOICES)
    # sub_category = models.CharField(max_length=1, choices=SUB_CATEGORY_CHOICES)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
    favorite_by = models.ManyToManyField(User, related_name="clothes_favorite_by", blank=True)
    outfit = models.ForeignKey(Outfit, related_name="outfit_clothes")
    top = models.CharField(max_length=200)
    left = models.CharField(max_length=200)
    detail = models.CharField(max_length=200)



# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=50,)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    height = models.CharField(max_length=3, choices=HEIGHT_CHOICES)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    bio = models.TextField(max_length=5000, default="Hello outfit of the day!")

    occupation = models.CharField(blank=True, max_length=50)
    follow_list = models.ManyToManyField(User, related_name="following")
    followed_by = models.ManyToManyField(User, related_name="followed")
    liked_outfit = models.ManyToManyField(Outfit, related_name="liked_outfit")

    picture = models.FileField(upload_to="images/profile", default='profile-default-pic-creative.png')
    longitude = models.FloatField(blank=True, default=0)
    latitude = models.FloatField(blank=True, default=0)

    def __unicode__(self):
        return 'Profile(id=' + str(self.id) + ')'


# Comment Model
class Comment(models.Model):
    content = models.CharField(max_length=200)
    post_id = models.ForeignKey(Outfit)
    created_by = models.ForeignKey(User, related_name="comment_created_by")
    creation_time = models.DateTimeField()


class Room(models.Model):
    """
    A room for people to chat in.
    """

    # Room title
    title = models.CharField(max_length=255)

    # If only "staff" users are allowed (is_staff on django's User)
    staff_only = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def group_name(self):
        """
        Returns the Channels Group name that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return "room-%s" % self.id
