from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    follows = models.ManyToManyField("self",related_name="followed_by",symmetrical=False,blank=True)
    date_modified = models.DateTimeField(User,auto_now=True)

    profile_image = models.ImageField(upload_to='images/',null=True,blank=True)
    
    bio = models.CharField(max_length=500, blank=True, null=True)
    website_link = models.CharField(max_length=100, blank=True, null=True)
    facebook_link = models.CharField(max_length=100, blank=True, null=True)
    instagram_link = models.CharField(max_length=100, blank=True, null=True)
    linkedin_link = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.user.username 


def createProfile(sender,instance,created,**kwargs):
    if created:
        user_profile = Profile(user = instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

post_save.connect(createProfile,sender = User)

class Talk(models.Model):
    user = models.ForeignKey(User,related_name='tweets',on_delete=models.DO_NOTHING)
    body = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True,related_name="likes")

    def num_of_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return (f"{self.user} " 
                f"{self.created:%Y-%m-%d %H:%M} - "
                f"{self.body}..."
                )

