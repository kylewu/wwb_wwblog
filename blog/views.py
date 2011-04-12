# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response,get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.template.context import RequestContext

from google.appengine.api import users

from blog.models import Post, Tag, Comment, Category, Tag_Post, Page
from blog.forms import CommentForm
from blog.setting import LIST_PER_PAGE, ADMIN
from blog.utils.object_list import object_list


def index(request):
    posts = Post.all().order('-create_time')
    
    #return test_list(request, queryset=posts, paginate_by=LIST_PER_PAGE, template_name='index.html', 
    #    extra_context={}, template_object_name='post') 
    return object_list(request,
                       template_object_name = 'post',
                       queryset = posts,
                       allow_empty = True,
                       extra_context = {},
                       template_name = 'index.html',
                       paginate_by = LIST_PER_PAGE,
                       )

def single_post(request, post_id):
    post = Post.get_by_id( int(post_id) )
    if not post:
        raise Http404
    form = CommentForm()
    if request.method == 'POST':

        if users.get_current_user():
            form = CommentForm(request.POST)

            if form.is_valid():
                 refresh_sys()
                 comment = form.save()
                 comment.author = users.get_current_user()
                 comment.post = post
                 comment.content = comment.content
                 comment.put()
            return HttpResponseRedirect('/post/%s/' %post_id)
        else:
            return HttpResponseRedirect('/')

    return render_to_response('single.html',
                              dictionary = { "post" : post, "form" : form, "user": users.get_current_user()},
                              )

def single_page(request, page_id):
    page = Page.get_by_id( int(page_id) )
    if not page:
        raise Http404

    return render_to_response('single.html',
                              dictionary = { "post" : page },
                              )

def list_category(request, category_id):
    category = Category.get_by_id( int(category_id) )

    posts = category.posts.order('-create_time')

    return object_list(request,
                       template_object_name = 'post',
                       queryset = posts,
                       extra_context = { 'cort':category, 'type':'Category' },
                       allow_empty = True,
                       template_name = 'page.html',
                       paginate_by = LIST_PER_PAGE,
                       )

def list_tag(request, tag_id):
    tag = Tag.get_by_id( int(tag_id) )

    posts = []
    for post in tag.posts:
        posts.append(post.post)

    return object_list(request,
                       template_object_name = 'post',
                       queryset = posts,
                       extra_context = { 'cort':tag, 'type':'Tag' },
                       allow_empty = True,
                       template_name = 'page.html',
                       paginate_by = LIST_PER_PAGE,
                       )

def about(request):
    post = Page.all().get()
    if post:
        return render_to_response('single.html',
                              dictionary = { "post" : Page.all().get() },
                              )
    else:
        return HttpResponseRedirect('/')
def feeds(request):
    return render_to_response('feeds/feeds.html',
                              dictionary = {"posts": Post.all().order('-create_time')[:10] },
                              )

def login(request):
    return HttpResponseRedirect(users.create_login_url('/'))

def logout(request):
    return HttpResponseRedirect(users.create_logout_url('/'))