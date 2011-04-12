# -*- coding: utf-8 -*-
# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django.conf.urls.defaults import *
from blog import setting

urlpatterns = patterns('',
     
     (r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':'static'}),
     (r'^theme/(?P<path>.*)$', 'django.views.static.serve',{'document_root':'templates/theme/%s'%setting.THEME}),
     
)

urlpatterns += patterns('blog.views',

    # index
    (r'^$', 'index'),
    (r'list/post', 'index'),
    
    # display one post or page
    (r'^post/(?P<post_id>\d+)/$', 'single_post'),
    (r'^page/(?P<page_id>\d+)/$', 'single_page'),
       
    # list posts in one category or tag
    (r'^category/(?P<category_id>\d+)/$', 'list_category'),
    (r'^tag/(?P<tag_id>\d+)/$', 'list_tag'),

    # login, logout
    (r'^login/$', 'login'),
    (r'^logout/$', 'logout'),
    
    (r'^about/$', 'about'),
    (r'^feeds/$', 'feeds'),
)

urlpatterns += patterns('blog.admin_views',

    # admin index
    (r'^admin/$', 'admin'),
    
    # admin list
    (r'^admin/post/$', 'admin_list_post'),
    (r'^admin/page/$', 'admin_list_page'),
    (r'^admin/tag/$', 'admin_list_tag'),
    (r'^admin/category/$', 'admin_list_category'),
    (r'^admin/link/$', 'admin_list_link'),
    
    # admin add
    (r'^post/add/$', 'admin_add_post'),
    (r'^page/add/$', 'admin_add_page'),
    (r'^tag/add/$', 'admin_add_tag'),
    (r'^category/add/$', 'admin_add_category'),
    (r'^link/add/$', 'admin_add_link'),

    # admin edit
    (r'^post/(?P<post_id>\d+)/edit/$', 'admin_edit_post'),
    (r'^page/(?P<page_id>\d+)/edit/$', 'admin_edit_page'),

    # admin delete
    (r'^post/(?P<post_id>\d+)/del/$', 'admin_del_post'),
    (r'^page/(?P<page_id>\d+)/del/$', 'admin_del_page'),
    #(r'^tag/(?P<tag_id>\d+)/del/$', 'admin_del_tag'),
    #(r'^category/(?P<category_id>\d+)/del/$', 'admin_del_category'),
    (r'^link/(?P<link_id>\d+)/del/$', 'admin_del_link'),
    
    #TODO /comment/(?P<post_id>\d+)/edit 
                         
)
