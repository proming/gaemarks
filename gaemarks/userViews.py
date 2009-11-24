# coding=UTF-8

from google.appengine.ext import db
from google.appengine.ext.db import GqlQuery, Key
from google.appengine.api import users
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from models import UserInfo
from forms import LoginForm, UserInfoForm, UserAuthForm
import gaemarks.tools as tools
import gaemarks.userApi as userApi

def userLoginView(request):
  context = Context({
  })
  
  if userApi.checkUserAuth(request):
    return HttpResponseRedirect('/')
  
  template = loader.get_template('html/login.html')
  return HttpResponse(template.render(context))

def userLogOutView(request):
  context = Context({
  })
  
  userApi.delUserAuth(request)
  
  template = loader.get_template('html/login.html')
  return HttpResponse(template.render(context))

def regUserView(request):
  context = Context({
  })
  
  template = loader.get_template('html/regUser.html')
  return HttpResponse(template.render(context))
  
def forgotRequestView(request):
  context = Context({
  })
  
  template = loader.get_template('html/forgotPasswd.html')
  return HttpResponse(template.render(context))
  
def resetPasswdView(request, key):
  context = Context({
  })
  #检查验证码是否存在
  user = userApi.getUserByChangeFlag(key)
  context.user = user
  template = loader.get_template('html/resetPasswd.html')
  return HttpResponse(template.render(context))
