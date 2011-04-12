# -*- coding: utf-8 -*-
from django import newforms
from google.appengine.ext.db import djangoforms

from blog.models import Post, Comment, Category, Tag, Page, Link

class LinkForm(djangoforms.ModelForm):

    class Meta:
        model = Link

class PostForm(djangoforms.ModelForm):
    
    tags = newforms.CharField(label=u'Tag', widget = newforms.TextInput, required = False)
    
    class Meta:
        model = Post
        exclude = ['author', 'read_count', 'create_time', 'update_time']

class PageForm(djangoforms.ModelForm):

    class Meta:
        model = Page
        exclude = ['author', 'read_count', 'create_time', 'update_time']

class CommentForm(djangoforms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['author', 'post', 'create_time', ]

class CategoryForm(djangoforms.ModelForm):

    class Meta:
        model = Category

class TagForm(djangoforms.ModelForm):

    class Meta:
        model = Tag