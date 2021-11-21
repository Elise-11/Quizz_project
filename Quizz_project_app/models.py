from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


''' 
Class: Profile 
This class allows to initialize profile table in the database.
A profile is created automatically when a user is created by the 
authentication form provided by django in the table User. 
'''
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


''' 
@receiver is a decorator that allows to call the following functions
(to create a profile and save it) each time a new user is saved 
'''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

''' 
Class: Images
This class allows to initialize images table in the database
'''
class Images(models.Model):
    img_name = models.IntegerField()
    img_description = models.TextField()
    img_mode = models.CharField(max_length=60)
    img_cell_type = models.CharField(max_length=60)
    img_component = models.CharField(max_length=60)
    img_doi = models.CharField(max_length=60)
    img_organism = models.CharField(max_length=60)


''' 
Class: Question
This class allows to initialize question table in the database
'''
class Question(models.Model):
    quest_id = models.IntegerField()
    quest = models.CharField(max_length=60)
    quest_type= models.CharField(max_length=60)
    quest_image_field = models.CharField(max_length=60)
    quest_point= models.IntegerField()


''' 
Class: Answers
This class allows to initialize answers table in the database
'''
class Answers(models.Model):
    answer_id = models.IntegerField()
    q_id = models.IntegerField()
    answer = models.CharField(max_length=60)
    definition = models.TextField()
