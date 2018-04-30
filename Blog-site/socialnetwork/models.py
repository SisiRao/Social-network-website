from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    post_content = models.TextField(max_length=2000)
    post_by    = models.ForeignKey(User, related_name="post_creators")
    post_time = models.DateTimeField()
    objects = models.Manager()

    def __unicode__(self):
        return 'Post(id=' + str(self.id) + ')'


class Comment(models.Model):
    comment_content = models.TextField(max_length=2000)
    comment_by    = models.ForeignKey(User, related_name="comment_creators")
    comment_time = models.DateTimeField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    objects = models.Manager()

    def __unicode__(self):
        return 'Comment(id=' + str(self.id) + ')'


class Profile(models.Model):
    bio = models.TextField(max_length=5000, default="Hi Y world!")
    picture = models.FileField(blank=True, default='default.jpg')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    follow_list = models.ManyToManyField(User, related_name="follower_followed")

    def __unicode__(self):
        return 'Profile(id=' + str(self.id) + ')'


