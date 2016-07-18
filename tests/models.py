# Testing models to create `Tracker` instances from.
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Post(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    body = models.TextField()
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)
