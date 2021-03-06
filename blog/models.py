from django.db import models
from django.utils.datetime_safe import real_datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_resized import ResizedImageField


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł")
    text = models.TextField(max_length=1000, verbose_name="Treść")
    created_at = models.DateTimeField(auto_now_add=True)
    image = ResizedImageField(size=[800, 800], upload_to='images/', force_format="jpeg", verbose_name="Zdjęcie (opcjonalne)", null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Wpis"

    class Meta:
        verbose_name = 'Wpisy'
        verbose_name_plural = 'Wpisy'

class Comment(models.Model):
    text = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return "Komentarz"
    
    class Meta:
        ordering = ["-created_at"]
        verbose_name = 'Komentarze'
        verbose_name_plural = 'Komentarze'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = ResizedImageField(size=[240, 240], null=True, upload_to='images/', force_format="jpeg", default="default.jpg")

    def __str__(self):
        return "Profil"

    class Meta:
        verbose_name = "Profile użytkownika"
        verbose_name_plural = "Profile użytkownika"


@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()