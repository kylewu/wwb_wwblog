# -*- coding: utf-8 -*-

from google.appengine.ext import db
from django.core.urlresolvers import reverse
import string

class Link(db.Model):
	title		  = db.StringProperty(required = True)
	link		  = db.LinkProperty(required = True)

	def get_absolute_url(self):
		 return "/link/%i/" % self.key().id()
	def __unicode__(self):
		return self.title

class Page(db.Model):
	author        = db.UserProperty()
	title		  = db.StringProperty(required = True)

	content		  = db.TextProperty(required = True)
	create_time   = db.DateTimeProperty(auto_now_add = True)
	update_time   = db.DateTimeProperty(auto_now = True)

	def get_absolute_url(self):
		 return "/page/%i/" % self.key().id()
    
	def __unicode__(self):
		return self.title
	
# one - many  (Post)
class Category(db.Model):
    title          = db.StringProperty(required = True)
    
    def get_absolute_url(self):
     return "/category/%i/" % self.key().id()

    def __unicode__(self):
        return self.title

# many - many  (Post)
class Tag(db.Model):
    title          = db.StringProperty(required = True)
    
    def get_absolute_url(self):
     return "/tag/%i/" % self.key().id()
    
    def __unicode__(self):
        return self.title

class Post(db.Model):
    author        = db.UserProperty()
    title         = db.StringProperty(required = True)

    category      = db.ReferenceProperty(Category, collection_name='posts')

    content       = db.TextProperty(required = True)
    create_time   = db.DateTimeProperty(auto_now_add = True)

    def get_absolute_url(self):
    	return "/post/%i/" % self.key().id()
   
	def __unicode__(self):
		return self.title


# many - one  (Post)
class Comment(db.Model):
    author        = db.UserProperty()

    content       = db.StringProperty(multiline = True)
    post          = db.ReferenceProperty(Post, collection_name='comments')
    create_time   = db.DateTimeProperty(auto_now_add = True)
    
    def get_absolute_url(self):
     return "/comment/%i/" % self.post.key().id()
    
class Tag_Post(db.Model):

    tag = db.ReferenceProperty(Tag,
                               required=True,
                               collection_name='posts',)
    post = db.ReferenceProperty(Post,
                               required=True,
                               collection_name='tags',)

