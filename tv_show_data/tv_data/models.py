from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class Show(models.Model):

    title = models.CharField(max_length=200)
    title_slugged = models.SlugField(unique=True)
    imdb_id = models.CharField(max_length=15)
    released = models.DateField(default=timezone.now)
    rated = models.CharField(max_length=10, default='TV-MA')
    poster_url = models.CharField(max_length=200, default='None')
    runtime = models.IntegerField(default=22)

    def save(self, *args, **kwargs):
        self.title_slugged = slugify(self.title)
        super(Show, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Episode(models.Model):
    show = models.ForeignKey(Show, on_delete=models.CASCADE)
    episode_title = models.CharField(max_length=200)
    air_date = models.DateField(default=timezone.now)
    rating = models.DecimalField(max_digits=4, decimal_places=2)
    number_of_ratings = models.IntegerField()
    episode_number = models.IntegerField()
    season = models.IntegerField()
    imdb_episode_id = models.CharField(max_length=20)