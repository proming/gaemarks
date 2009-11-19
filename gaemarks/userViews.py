# coding=UTF-8

from google.appengine.ext import db
from google.appengine.ext.db import GqlQuery
from google.appengine.api import users
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from models import UserInfo
from forms import LoginForm, UserInfoForm, UserAuthForm
import tools
import userApi

def userLoginView(request):
  context = Context({
  })
  
  if userApi.checkUserAuth(request):
    form = UserAuthForm(request.POST)
    context.userId = form.cleaned_data['userId']
    context.authCode = form.cleaned_data['authCode']
  
  template = loader.get_template('html/login.html')
  return HttpResponse(template.render(context))

def regUserView(request):
  context = Context({
  })
  
  context.loginErr='none'
  
  if request.method == 'POST':
    form = UserInfoForm(request.POST)
    if form.is_valid():
      if userApi.checkUserId(form.cleaned_data['userId']):
        context.loginErr='block'
        context.errMsg = '用户名已存在！'
      elif userApi.checkEmail(form.cleaned_data['email']):
        context.loginErr='block'
        context.errMsg = '邮箱已存在！'
      else:
        userInfo = UserInfo()
        userInfo.userId = form.cleaned_data['userId']
        userInfo.email = form.cleaned_data['email']
        userInfo.passwd = form.cleaned_data['passwd']
        userInfo.put();
        
        return HttpResponseRedirect('/login')
    else:
      context.loginErr='block'
      context.errMsg = '录入信息错误，请重新录入！'
  
  template = loader.get_template('html/regUser.html')
  return HttpResponse(template.render(context))


