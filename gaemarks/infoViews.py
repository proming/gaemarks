# coding=UTF-8

from google.appengine.ext import db
from google.appengine.ext.db import GqlQuery
from google.appengine.api import users
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from models import UserInfo
from forms import LoginForm, UserInfoForm, UserAuthForm
import gaemarks.tools as tools
import gaemarks.userApi as userApi

def dashboardView(request):
  context = userApi.getUserAuthContext(request)
  
  if context:
    template = loader.get_template('html/dashboard.html')
    return HttpResponse(template.render(context))
    
  return HttpResponseRedirect('/login')
  
def userinfoView(request):
  context = userApi.getUserAuthContext(request)
  
  if context:
    template = loader.get_template('html/userinfo.html')
    return HttpResponse(template.render(context))
    
  return HttpResponseRedirect('/login')
