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
  context = Context({
  })
  
  if userApi.checkUserAuth(request):
    if request.method == 'POST':
      form = UserAuthForm(request.POST)
    else:
      form = UserAuthForm(request.COOKIES)
    if form.is_valid():
      context.userLoginId = form.cleaned_data['userLoginId']
      context.userLoginAuth = form.cleaned_data['userLoginAuth']
    
    context.user = userApi.getUserByUserId(context.userLoginId)
    context.userLoginImg = tools.getUserImgUrl(context.user.email, 20)
    context.userLoginImg120 = tools.getUserImgUrl(context.user.email, 120)
    context.userUID = context.user.key().id()
    
    template = loader.get_template('html/dashboard.html')
    return HttpResponse(template.render(context))
    
  return HttpResponseRedirect('/login')
  
def userinfoView(request):
  context = Context({
  })
  
  if userApi.checkUserAuth(request):
    if request.method == 'POST':
      form = UserAuthForm(request.POST)
    else:
      form = UserAuthForm(request.COOKIES)
    if form.is_valid():
      context.userLoginId = form.cleaned_data['userLoginId']
      context.userLoginAuth = form.cleaned_data['userLoginAuth']
    
    context.user = userApi.getUserByUserId(context.userLoginId)
    context.userLoginImg = tools.getUserImgUrl(context.user.email, 20)
    context.userLoginImg120 = tools.getUserImgUrl(context.user.email, 120)
    context.userUID = context.user.key().id()
    
    template = loader.get_template('html/userinfo.html')
    return HttpResponse(template.render(context))
    
  return HttpResponseRedirect('/login')
