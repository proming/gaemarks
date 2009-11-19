
from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^t1/', include('t1.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/(.*)', admin.site.root),\
    (r'^login$','gaemarks.userViews.userLoginView'),
    (r'^login.action$','gaemarks.userApi.userLogin'),
    (r'^regUser$','gaemarks.userViews.regUserView'),
    (r'^regUser.action$','gaemarks.userApi.regUser'),
)
