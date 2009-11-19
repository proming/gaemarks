# coding=UTF-8

from google.appengine.ext import db
from google.appengine.ext.db import GqlQuery
from google.appengine.api import users
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from models import UserInfo
from forms import LoginForm, UserInfoForm, UserAuthForm
import tools
import json

def userLogin(request):
  reponse = dict()
  reponse['status'] = 0
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      userId = form.cleaned_data['userId']
      passwd = form.cleaned_data['passwd']
      if authService(userId, passwd):
        authCode = tools.getAuthCode(userId, tools.getUserSid(userId))
        tools.addToSession(userId + ":" + tools.getUserSid(userId), authCode)
        reponse['status'] = 1
        reponse['authCode'] = authCode
      else:
        reponse['msg'] = '用户名或密码错误，请重新录入！'
    else:
        reponse['msg'] = '用户名或密码错误，请重新录入！'

  return HttpResponse(json.dumps(reponse))
  
def checkUserAuth(request):
  if request.method == 'POST':
    form = UserAuthForm(request.POST)
    if form.is_valid():
      userId = form.cleaned_data['userId']
      authCode = form.cleaned_data['authCode']
      if tools.getUserAuth(userId, tools.getUserSid(userId)) == authCode:
        return True;
  return False;

def regUser(request):  
  if request.method == 'POST':
    form = UserInfoForm(request.POST)
    if form.is_valid():
      if checkUserId(form.cleaned_data['userId']):
        context.loginErr='block'
        context.errMsg = '用户名已存在！'
      elif checkEmail(form.cleaned_data['email']):
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
  
def authService(userId, passwd):
  query = UserInfo.all()
  query.filter('userId = ', userId).filter('passwd = ', passwd)
  if query.count() == 0:
    return False;
  else:
    return True;

def checkUserId(userId):
  query = UserInfo.all()
  query.filter('userId = ', userId)
  if query.count() == 0:
    return False;
  else:
    return True;
    
def checkEmail(email):
  query = UserInfo.all()
  query.filter('email = ', email)
  if query.count() == 0:
    return False;
  else:
    return True;

