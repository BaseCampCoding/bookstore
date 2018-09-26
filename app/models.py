from django.db import models
from django.urls import reverse
import random


class Author(models.Model):
    name = models.TextField()

    class Meta:
        default_related_name = 'authors'
        ordering = ['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        raise RuntimeError('get_absolute_url is gone now =). Use the {% url ... %} template tag.')


class BookManager(models.Manager):
    pass


class BookOfTheDayManager(models.Manager):
    def _all_ids(self):
        return self.get_queryset().values_list('id', flat=True)

    def _random_id(self):
        return random.choice(self._all_ids())

    def get(self):
        return self.get_queryset().get(id=self._random_id())


class Book(models.Model):
    title = models.TextField()
    authors = models.ManyToManyField(Author)
    price = models.FloatField()
    cover_image = models.ImageField(upload_to='book_covers')
    description = models.TextField()

    objects = BookManager()
    of_the_day = BookOfTheDayManager()

    class Meta:
        default_related_name = 'books'
        ordering = ['id']

    def __str__(self):
        return f"{self.title} by {', '.join(a.name for a in self.authors.all())}"

    def get_absolute_url(self):
        raise RuntimeError('get_absolute_url is gone now =). Use the {% url ... %} template tag.')

    def authors_ids(self):
        return self.authors.all().values_list('id', flat=True)
