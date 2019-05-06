from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Post


class PostSitemap(Sitemap):

    def items(self):
        return Post.objects.all().order_by("-pk")


class StaticViewSitemap(Sitemap):
    def items(self):
        return ['index', 'aboutUs', 'contact']

    def location(self, obj):
        return reverse("post:%s" % obj)
