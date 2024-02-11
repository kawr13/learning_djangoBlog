from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
# Create your models here.


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    images = models.FileField(upload_to='media/photos/', blank=True, null=True)

    def __str__(self):
        return self.username


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()\
            .filter(status=Post.Status.PUBLISHED)


class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    body = models.TextField()
    publish = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)
    images = models.ImageField(upload_to='media/photos/', blank=True, null=True)

    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-publish',)
        indexes = (
            models.Index(fields=('-publish',)),
        )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogapp:blog_detailed',
                       args=(self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug))


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    username = models.CharField(max_length=80)
    body = models.TextField()
    email = models.EmailField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)
        indexes = (
            models.Index(fields=('created',)),
        )

    def __str__(self):
        return f'Comment by {self.username} on {self.post.title}'

