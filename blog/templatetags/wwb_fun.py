# -*- coding: utf-8 -*-
from django.template import Library
from google.appengine.api import users
import string

from blog import setting
from blog.models import Post, Page, Tag, Link, Comment, Category

register = Library()

@register.filter
def safe(value):
    from blog.utils.safestring import mark_safe
    return mark_safe(value)

@register.simple_tag
def wwb_bloginfo(obj):
    args = {
            'name': '%s'%setting.NAME,
            'theme': '%s'%setting.THEME,
            'description': '%s'%setting.DESCRIPTION,
            'url': '%s'%setting.URL,
            'version': '%s'%setting.VERSION,
            'rss_url': '/feeds',
            'atom_url': '/feeds',
            'pingback_url': '/',
            }
    return args[obj]

@register.simple_tag
def wwb_list_category():
    html = ''
    for category in Category.all()[:10]:
        html += '<li><a href="%s">%s ( %d )</a></li>'%(category.get_absolute_url(), category.title.encode('utf-8'), category.posts.count()) 
    return html

@register.simple_tag
def wwb_list_post():   
    html = ''
    for post in Post.all().order('-create_time')[:10]:
        html += '<li><a href=\"%s">%s</a></li>'%(post.get_absolute_url(), post.title.encode('utf-8'))
    return html

@register.simple_tag
def wwb_list_page():   
    html = ''
    for page in Page.all()[:10]:
        html += '<li><a href=\"%s">%s</a></li>'%(page.get_absolute_url(), page.title.encode('utf-8'))
    return html

@register.simple_tag
def wwb_list_comment():   
    html = ''
    for comment in Comment.all()[:10]:
        html += '<li><a href=\"%s">%s</a></li>'%(comment.post.get_absolute_url(), comment.content.encode('utf-8'))
    return html
        
@register.simple_tag
def wwb_list_tag():   
    html = ''
    for tag in Tag.all():
        html += '<li><a href=\"%s">%s</a></li>'%(tag.get_absolute_url(), tag.title.encode('utf-8'))
    return html

@register.simple_tag
def wwb_list_tag_cloud():   
    html = ''
    for tag in Tag.all():
        html += ''
    return html

@register.simple_tag
def wwb_list_link():   
    html = ''
    for link in Link.all():
        html += '<li><a href=\"%s">%s</a></li>'%(link.link.encode('utf-8'), link.title.encode('utf-8'))
    return html

@register.simple_tag
def wwb_list_admin():   
    html = ''    

    user = users.get_current_user()
    if user is None:
        html += '<li><a href="/login/">Sign in or register</a></li>'
    else:
        html += '<p>Hello, %s </p>'%user.nickname()
        if users.is_current_user_admin():
            html += '<p><a href="/admin">Admin</a></p>'
    return html

@register.simple_tag
def wwb_show_tag_link(post):
    html = ''
    if post.tags.count():
        for tp in post.tags:
            html += '<a href="%s">%s</a> '%(tp.tag.get_absolute_url(), tp.tag.title.encode('utf-8'))
    else:
        html += 'None'
    return html

@register.simple_tag
def wwb_show_comment_link(post):
    html = ''
    if post.category:
        if post.comments.count() <= 1:
            html += str(post.comments.count()) + ' comment'
        else:
            html += str(post.comments.count()) + ' comments'
    return html
     
@register.simple_tag
def wwb_show_edit_link(obj):
    html = ''
    if users.is_current_user_admin():
        if not obj: return ''
        html += '<span class="editpost"><a href="' + obj.get_absolute_url() +'edit">Edit</a></span>'
    return html

