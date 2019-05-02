from . models import SubCategory, Post


def catsBase(request):
    return {'catsBase': SubCategory.objects.filter(priority=3)}


def recent(request):
    posts = Post.objects.all().order_by('-pk')
    recent_in = posts[:3]
    return {'recent': recent_in}