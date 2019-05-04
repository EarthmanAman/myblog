from django.db import models
from django.contrib.sites.models import Site
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField
from django.contrib.sitemaps import ping_google
from accounts.models import Author


class Category(models.Model):
    objects = models.Manager()
    date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=500, blank=True, null=True)
    pic = models.ImageField(blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def count(self):
        countIn = 0
        for sub in self.subcategory_set.all():
            countIn += sub.post_set.count()
        return countIn


class SubCategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    name = models.CharField(max_length=500, blank=True, null=True)
    pic = models.ImageField(blank=True, null=True)
    objects = models.Manager()

    priority = models.IntegerField(default=1)

    def __str__(self):
        return str(self.category.name) + " " + str(self.name)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True)
    authorView = RichTextField(blank=True, null=True)

    subCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True)
    views = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)
    title = RichTextField()
    description = models.TextField()
    content = RichTextField()
    pic = models.ImageField(blank=True, null=True)
    objects = models.Manager()

    featured = models.BooleanField(default=False)
    lead = models.BooleanField(default=False)

    slug = models.SlugField(blank=True, null=True)
    sites = models.ManyToManyField(Site)

    def __str__(self):
        return str(self.subCategory.category.name) + " " + str(self.subCategory.name) + " " + str(self.title)

    def get_absolute_url(self):
        return reverse("post:read", kwargs={'slug': self.slug})

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        try:
            ping_google()
        except Exception:
            pass
    # class Meta:
    #     ordering = ["-date"]

class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=3000)
    message = models.TextField()
    date = models.DateTimeField(default=timezone.datetime.now)

    def __str__(self):
        return self.email + " - " + self.subject


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)