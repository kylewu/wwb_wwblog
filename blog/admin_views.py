# -*- coding: utf-8 -*-
from blog import setting
from blog.forms import PostForm, CategoryForm, CommentForm, PageForm, TagForm, \
    LinkForm
from blog.models import Post, Tag, Comment, Category, Tag_Post, Page, Link
from blog.utils.object_list import object_list
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from google.appengine.api import users
from google.appengine.ext import db
import string

def admin(request):
    if users.is_current_user_admin():
        return render_to_response('admin/index.html',)
    else:
        return HttpResponseRedirect('/')

# Post Functions
def admin_add_post(request):

    if users.is_current_user_admin():
        if request.method == 'GET':
            form = PostForm()
            
        elif request.method == 'POST':
            form = PostForm(request.POST)
            
            if form.is_valid():
                post = form.save(commit=False)
                post.author = users.get_current_user()
                post.put()
                
                tagText = request.POST['tags']
                tags = tagText.split(',')
                for tag in tags:
                    if tag:
                        tag = string.lower(string.strip(tag))
                        
                        t = Tag.all().filter("title = ", unicode(tag, "utf-8")).get()
                        if not t:
                            t = Tag(title=unicode(tag, "utf-8"))
                            t.put()
                        Tag_Post(tag=t, post=post).put()

                return HttpResponseRedirect('/admin')

        return render_to_response('admin/edit.html',
                                        dictionary={ 'form':form ,
                                                         'type': 'Add Post',
                                                     },
                                      context_instance=RequestContext(request)
                                    )
    else:
        return HttpResponseRedirect('/')

def admin_edit_post(request, post_id):
    
    if users.is_current_user_admin():
        
        post = Post.get_by_id(int(post_id))
        if not post:
            raise Http404
        
        if request.method == 'GET':
            tp = Tag_Post.all().filter('post', post)
            
            tags = ''
            # Get all tags
            for tag in tp:
                tags += tag.tag.title + ','
                
            form = PostForm({'title':post.title, 'category':post.category.key(), 'content':post.content, 'tags':tags})
            
        elif request.method == 'POST':
            
            form = PostForm(request.POST)
            
            if form.is_valid():
                
                # delete related tag_post
                for tp in post.tags:
                    tp.delete()

                p = form.save(commit=False)
                post.author = users.get_current_user()
                post.category = p.category
                post.content = p.content
                post.put()

                # add tag_post
                tagText = request.POST['tags']
                if tagText:
                    tags = tagText.split(',')
                    for tag in tags:
                        if tag:
                            tag = string.lower(string.strip(tag))

                            t = Tag.all().filter("title = ", unicode(tag, "utf-8")).get()
                            if not t:

                                t = Tag(title=unicode(tag, "utf-8"))
                                t.put()
                            Tag_Post(tag=t, post=post).put()

            return HttpResponseRedirect('/admin')
        
        return render_to_response('admin/edit.html',
                                      dictionary={ 'form':form,
                                                    'type': 'Edit Post',
                                                     },
                                      context_instance=RequestContext(request)
                                    )
    else:
        return HttpResponseRedirect('/')
    
def admin_list_post(request):
    if users.is_current_user_admin():
        
        return object_list(request,
                       template_object_name='obj',
                       queryset=Post.all().order('-create_time'),
                       allow_empty=True,
                       extra_context={'type': 'post'},
                       template_name='admin/list.html',
                       paginate_by=setting.ADMIN_LIST_PER_PAGE,
                       )
    else:
        return HttpResponseRedirect('/')
    
def admin_del_post(request, post_id):
    if users.is_current_user_admin():
        
        post = Post.get_by_id(int(post_id))
        if not post:
            raise Http404
        else:
            post.delete()
        return HttpResponseRedirect('/admin')
    else:
        return HttpResponseRedirect('/')

# Page Functions
def admin_add_page(request):

    if users.is_current_user_admin():
        if request.method == 'GET':
            form = PageForm()
            
        elif request.method == 'POST':
            form = PageForm(request.POST)
            if form.is_valid():
                page = form.save(commit=False)
                page.author = users.get_current_user()
                page.content
                page.put()
                return HttpResponseRedirect('/admin')
        return render_to_response('admin/edit.html',
                                      dictionary={ 'form':form,
                                                    'type': 'Add Page',
                                                    },
                                      context_instance=RequestContext(request)
                                    )
    else:
        return HttpResponseRedirect('/')

def admin_edit_page(request, page_id):
    if users.is_current_user_admin():
        page = Page.get_by_id(int(page_id))
        
        if request.method == 'GET':
            form = PageForm({'title':page.title, 'content':page.content, })
            
        elif request.method == 'POST':
            form = PageForm(request.POST)
            if form.is_valid():
                p = form.save(commit=False)
                page.title = p.title
                page.content = p.content
                page.put()

            return HttpResponseRedirect('/admin')
        
        return render_to_response('admin/edit.html',
                                      dictionary={'form' : form,
                                                    'type' : 'Edit Page',
                                                     },
                                      context_instance=RequestContext(request)
                                    )
    else:
        return HttpResponseRedirect('/')
    
def admin_list_page(request):
    if users.is_current_user_admin():
        
        return object_list(request,
                       template_object_name='obj',
                       queryset=Page.all().order('-create_time'),
                       allow_empty=True,
                       extra_context={'type': 'page'},
                       template_name='admin/list.html',
                       paginate_by=setting.ADMIN_LIST_PER_PAGE,
                       )
    else:
        return HttpResponseRedirect('/')
    
def admin_del_page(request, page_id):
    if users.is_current_user_admin():
        
        page = Page.get_by_id(int(page_id))
        if not page:
            raise Http404
        else:
            page.delete()
        return HttpResponseRedirect('/admin')
    else:
        return HttpResponseRedirect('/')

# Category Functions
def admin_add_category(request):

    if users.is_current_user_admin():
        if request.method == 'GET':
            form = CategoryForm()
            
        elif request.method == 'POST':
            form = CategoryForm(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.put()
            return HttpResponseRedirect('/admin')
        
        return render_to_response('admin/edit.html',
                                      dictionary={ 'form':form,
                                                    'type': 'Add Category',
                                                    },
                                      context_instance=RequestContext(request)
                                    )
    else:
        return HttpResponseRedirect('/')

# Link Functions
def admin_add_link(request):

    if users.is_current_user_admin():
        if request.method == 'GET':
            form = LinkForm()
        
        elif request.method == 'POST':
            form = LinkForm(request.POST)  
            if form.is_valid():
                link = form.save()
                link.put()
            return HttpResponseRedirect('/admin')
        return render_to_response('admin/edit.html',
                                      dictionary={ 'form':form,
                                                    'type': 'Add Link',
                                                     },
                                      context_instance=RequestContext(request)
                                    )
    else:
        return HttpResponseRedirect('/')
    
def admin_list_link(request):
    if users.is_current_user_admin():
        
        return object_list(request,
                       template_object_name='obj',
                       queryset=Link.all(),
                       allow_empty=True,
                       extra_context={'type': 'link'},
                       template_name='admin/list.html',
                       paginate_by=setting.ADMIN_LIST_PER_PAGE,
                       )
    else:
        return HttpResponseRedirect('/')

def admin_del_link(request, link_id):
    if users.is_current_user_admin():
        
        link = Link.get_by_id(int(link_id))
        if not link:
            raise Http404
        else:
            link.delete()
        return HttpResponseRedirect('/admin')
    else:
        return HttpResponseRedirect('/')
    
#Tag Functions
def admin_add_tag(request):

    if users.is_current_user_admin():
        if request.method == 'GET':
            form = TagForm()
            
        elif request.method == 'POST':
            form = TagForm(request.POST)
            if form.is_valid():
                tag = form.save(commit=False)
                tag.title = string.lower(tag.title)
                tag.put()
            return HttpResponseRedirect('/admin')
        return render_to_response('admin/edit.html',
                                      dictionary={ 'form':form,
                                                    'type': 'Add Tag',
                                                     },
                                      context_instance=RequestContext(request)
                                    )
    else:
        return HttpResponseRedirect('/')
    
def admin_list_tag(request):
    if users.is_current_user_admin():
        
        return object_list(request,
                       template_object_name='obj',
                       queryset=Tag.all(),
                       allow_empty=True,
                       extra_context={'type': 'tag'},
                       template_name='admin/list.html',
                       paginate_by=setting.ADMIN_LIST_PER_PAGE,
                       )
    else:
        return HttpResponseRedirect('/')
    
def admin_list_category(request):
    if users.is_current_user_admin():
        
        return object_list(request,
                       template_object_name='obj',
                       queryset=Category.all(),
                       allow_empty=True,
                       extra_context={'type': 'category'},
                       template_name='admin/list.html',
                       paginate_by=setting.ADMIN_LIST_PER_PAGE,
                       )
    else:
        return HttpResponseRedirect('/')
    
