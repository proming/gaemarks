
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
    (r'^$','gaemarks.infoViews.dashboardView'),
    (r'^userinfo$','gaemarks.infoViews.userinfoView'),
    (r'^logout$','gaemarks.userViews.userLogOutView'),
    (r'^login$','gaemarks.userViews.userLoginView'),
    (r'^regUser$','gaemarks.userViews.regUserView'),
    (r'^forgotPasswd$','gaemarks.userViews.forgotRequestView'),
    (r'^resetPasswd/(?P<key>.+)$','gaemarks.userViews.resetPasswdView'),
    (r'^bookmark$','gaemarks.siteViews.siteView'),
    (r'^site/about$','gaemarks.siteViews.siteView'),
    (r'^site/guestbook$','gaemarks.siteViews.siteView'),
    (r'^site/help$','gaemarks.siteViews.siteView'),
    #action
    (r'^login.action$','gaemarks.userApi.userLogin'),
    (r'^regUser.action$','gaemarks.userApi.regUser'),
    (r'^forgotPasswd.action$','gaemarks.userApi.forgotRequest'),
    (r'^resetPasswd.action$','gaemarks.userApi.resetPasswd'),
    (r'^updateInfo.action$','gaemarks.infoApi.updateInfo'),
    (r'^changePasswd.action$','gaemarks.infoApi.changePasswd'),
)
