from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from PIL import Image


class Ticket(models.Model):  # ticket model
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=2048)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)
    IMAGE_MAX_SIZE = (800, 800)

    def resize_image(self):
        image = Image.open(self.image)
        image.thumbnail(self.IMAGE_MAX_SIZE)
        # sauvegarde de l’image redimensionnée dans le système de fichiers
        # ce n’est pas la méthode save() du modèle !
        image.save(self.image.path)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.resize_image()

class Review(models.Model):  # ticket model
    ticket = models.ForeignKey(to=Ticket,on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[ MinValueValidator(0),
                                                           MaxValueValidator(5)])
    content = models.CharField(max_length=5000)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length = 8192, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class UserFollows(models.Model):
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='following')
    followed_user = models.ForeignKey(to=settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='followed_by')
    class Meta:
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ['user', 'followed_user',]
