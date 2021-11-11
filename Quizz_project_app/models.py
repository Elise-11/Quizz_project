from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Images(models.Model):
    img_name = models.IntegerField()
    img_description = models.TextField()
    img_mode = models.CharField(max_length=60)
    img_cell_type = models.CharField(max_length=60)
    img_component = models.CharField(max_length=60)
    img_doi = models.CharField(max_length=60)
    img_organism = models.CharField(max_length=60)


class Question(models.Model):
    quest_id = models.IntegerField()
    quest = models.CharField(max_length=60)
    quest_type= models.CharField(max_length=60)
    quest_image_field = models.CharField(max_length=60)
    quest_point= models.IntegerField()
    n_answer = models.IntegerField()
    n_image = models.IntegerField()


class Answers(models.Model):
    answer_id = models.IntegerField()
    q_id = models.IntegerField()
    answer = models.CharField(max_length=60)
    definition = models.TextField()


class AnswerUser(models.Model):
    user_question = models.CharField(max_length=120)
    good_answer_id = models.IntegerField()
