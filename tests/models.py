# Testing models to create `Tracker` instances from.
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    slug = models.SlugField()
    body = models.TextField()
    published = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.title)

    def save(
        self, force_insert=False, force_update=False, using=None,
        update_fields=None
    ):
        if not self.slug:
            self.slug = slugify(self.title)

        super(Post, self).save(
            force_insert=False, force_update=False, using=None,
            update_fields=None
        )
