from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import (
    Category,
    Contact,
    Post,
    SubCategory,
)

from comment.models import Comment


def cat_checker(posts_in):
    posts = []
    if len(posts_in) > 3:
        two_post = [posts_in[1], posts_in[2]]
        posts = posts_in[3:]
    elif len(posts_in) == 2:
        two_post = posts_in[1:]
    else:
        two_post = []
    return two_post, posts


def more_cat(request, sub_id):
    sub_cat = SubCategory.objects.get(pk=sub_id)
    all_posts = Post.objects.filter(subCategory=sub_cat)
    paginator = Paginator(all_posts, 2)  # Show 25 contacts per page

    page = request.GET.get('page')
    pag_posts = paginator.get_page(page)
    return render(request, './post/search_result.html', {
        'posts': pag_posts,
        'title': "Posts",
        'categories': Category.objects.all()})


def index(request):
    template_name = "./post/index.html"
    most_view_posts = Post.objects.filter(lead=True).order_by("-pk")
    most_view = most_view_posts[:2]
    most_read = Post.objects.all().order_by("-views")
    posts = Post.objects.all().order_by('-pk')
    recent = posts[:3]
    context = {'mostRead': most_view,
               'recent': recent,
               'most_read': most_read[:4],
               'categories': Category.objects.all(),
               'featured_posts': Post.objects.filter(featured=True).order_by("-pk")}
    return render(request, template_name, context)


def read(request, slug):

    template_name = "./post/read.html"

    """Saving views"""
    post = Post.objects.get(slug=slug)
    post.views += 1
    post.save()

    """most read post and parent comments"""
    most_read = Post.objects.all().order_by("-views")
    comments = Comment.objects.filter(post=post, parent=None)

    """adding comments"""
    if request.method == "POST":
        message = request.POST.get('message')
        if request.POST.get('parent'):
            parent = Comment.objects.get(pk=int(request.POST.get('parent')))
            comment = Comment(user=request.user, post=post, content=message, parent=parent)
            comment.save()
        else:
            comment = Comment(user=request.user, post=post, content=message)
            comment.save()

    """context"""
    context = {'post': post,
               'mostRead': most_read[:4],
               'featured_posts': Post.objects.filter(featured=True).order_by("-pk"),
               'catsIn': Category.objects.all(),
               'comments': comments,
               }
    return render(request, template_name, context)


def edit_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.method == "POST":
        if request.user == comment.user:
            message = request.POST.get("message")
            comment.content = message
            comment.save()
    return render(request, './post/editComment.html', {'comment': comment})


def remove_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.method == "POST":
        if request.user == comment.user:
            comment.delete()
    return render(request, './post/deleteComment.html', {'comment': comment})


def sub_category(request, sub_id):
    sub_cat = SubCategory.objects.get(pk=sub_id)
    most_view = Post.objects.all().order_by("-views")
    posts_in = sub_cat.post_set.all().order_by('-pk')
    first = posts_in.first()
    two_post, posts = cat_checker(posts_in)
    if request.method == "POST":
        return redirect(reverse("post:more_cat", kwargs={'sub_id': sub_id}))
    template_name = "./post/sub_category.html"
    context = {'subCategory': sub_cat,
               'posts': posts,
               'first': first,
               'two_post': two_post,
               'most_view': most_view[:4],
               'cats': Category.objects.all(),
               }
    return render(request, template_name, context)


def popular(request):
    posts_in = Post.objects.all().order_by('-views')
    first = posts_in.first()
    most_view = Post.objects.all().order_by("-views")
    two_post, posts = cat_checker(posts_in)

    template_name = "./post/popular.html"
    context = {
               'posts': posts,
               'first': first,
               'two_post': two_post,
               'most_view': most_view[:4],
               'cats': Category.objects.all(),
               }
    return render(request, template_name, context)


def about_us(request):
    most_read = Post.objects.all().order_by("-views")
    template_name = "./post/aboutUs.html"
    context = {'most_read': most_read[:4]}
    return render(request, template_name, context)


def contact(request):
    template_name = "./post/contact.html"
    if request.method == "POST":
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        con = Contact(email=email, subject=subject, message=message)
        con.save()
    return render(request, template_name)
