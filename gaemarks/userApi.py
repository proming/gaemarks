# coding=UTF-8

from google.appengine.ext import db
from google.appengine.ext.db import GqlQuery
from google.appengine.api import users
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from models import UserInfo
from forms import LoginForm, UserInfoForm, UserAuthForm, ForgotRequestForm, PasswdResetForm
import gaemarks.tools as tools
from django.utils import simplejson as json

def userLogin(request):
  reponse = dict()
  reponse.update(status = 0, msg = '用户名或密码错误，请重新录入！')
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      userId = form.cleaned_data['userId']
      passwd = form.cleaned_data['passwd']
      if authService(userId, passwd):
        authCode = tools.getAuthCode(userId)
        tools.addSession(userId, authCode)
        reponse.update(status = 1, userLoginId= userId, userLoginAuth=authCode, msg='登录成功！')
        
  return HttpResponse(json.dumps(reponse), mimetype='application/json')

def regUser(request):
  reponse = dict()
  reponse.update(status = 0, msg = '录入信息错误，请重新录入！')
  msg = ''
  if request.method == 'POST':
    form = UserInfoForm(request.POST)
    if form.is_valid():
      if checkUserId(form.cleaned_data['userId']):
        msg = '用户名已存在!'
      elif checkEmail(form.cleaned_data['email']):
        msg = '邮箱已存在!'
      else:
        userInfo = UserInfo()
        userInfo.userId = form.cleaned_data['userId']
        userInfo.email = form.cleaned_data['email']
        userInfo.passwd = form.cleaned_data['passwd']
        userInfo.create();
        msg = '注册成功!'
        reponse.update(status = 1)
  if msg != '':
    reponse.update(msg = msg)
  return HttpResponse(json.dumps(reponse),mimetype='application/json')

def delUser(request):
  reponse = dict()
  reponse.update(status = 0, msg = '请重新登录系统！')
  formPost = UserAuthForm()
  formCookie = UserAuthForm()
  if request.POST:
    formPost = UserAuthForm(request.POST)
  if request.COOKIES:
    formCookie = UserAuthForm(request.COOKIES)
  
  if formCookie.is_valid():
    userLoginId = formCookie.cleaned_data['userLoginId']
    userLoginAuth = formCookie.cleaned_data['userLoginAuth']
    if tools.getSession(userLoginId) == userLoginAuth:
      tools.delSession(userLoginId)
      userInfo = getUserByUserId(userLoginId)
      userInfo.delete()
      reponse.update(status = 1, msg = '注销用户成功！')
      return HttpResponse(json.dumps(reponse),mimetype='application/json');
      
  if formPost.is_valid():
    userLoginId = formPost.cleaned_data['userLoginId']
    userLoginAuth = formPost.cleaned_data['userLoginAuth']
    if tools.getSession(userLoginId) == userLoginAuth:
      tools.delSession(userLoginId)
      userInfo = getUserByUserId(userLoginId)
      userInfo.delete()
      reponse.update(status = 1, msg = '注销用户成功！')
      return HttpResponse(json.dumps(reponse),mimetype='application/json');
      
  return HttpResponse(json.dumps(reponse),mimetype='application/json');
  
def forgotRequest(request):
  reponse = dict()
  reponse.update(status = 0, msg = '用户名或邮箱错误，请重新录入！')
  if request.method == 'POST':
    form = ForgotRequestForm(request.POST)
    if form.is_valid():
      userId = form.cleaned_data['userId']
      email = form.cleaned_data['email']
      if checkIdAndEmail(userId, email):
        changeFlag = tools.sendEmail(userId, email)
        setChangeFlag(userId, changeFlag)
        reponse.update(status = 1, msg='邮件已发送到您的邮箱，请及时重新设置密码！')
        
  return HttpResponse(json.dumps(reponse), mimetype='application/json')

def resetPasswd(request):
  reponse = dict()
  reponse.update(status = 0, msg = '录入信息错误，请重新录入！')
  msg = ''
  if request.method == 'POST':
    form = UserInfoForm(request.POST)
    if form.is_valid():
      if not checkIdAndEmail(form.cleaned_data['userId'], form.cleaned_data['email']):
        msg = '用户名或邮箱错误，请重新录入！'
      else:
        userInfo = getUserByUserId(form.cleaned_data['userId'])
        userInfo.passwd = form.cleaned_data['passwd']
        userInfo.changeFlag = ''
        userInfo.put();
        msg = '密码重设成功!'
        reponse.update(status = 1)
  if msg != '':
    reponse.update(msg = msg)
  return HttpResponse(json.dumps(reponse),mimetype='application/json')

def checkUserAuth(request):
  formPost = UserAuthForm()
  formCookie = UserAuthForm()
  if request.POST:
    formPost = UserAuthForm(request.POST)
  if request.COOKIES:
    formCookie = UserAuthForm(request.COOKIES)
  
  if formCookie.is_valid():
    userLoginId = formCookie.cleaned_data['userLoginId']
    userLoginAuth = formCookie.cleaned_data['userLoginAuth']
    if tools.getSession(userLoginId) == userLoginAuth:
      tools.addSession(userLoginId, userLoginAuth)
      return True;
      
  if formPost.is_valid():
    userLoginId = formPost.cleaned_data['userLoginId']
    userLoginAuth = formPost.cleaned_data['userLoginAuth']
    if tools.getSession(userLoginId) == userLoginAuth:
      tools.addSession(userLoginId, userLoginAuth)
      return True;
   
  return False;

def getUserAuthContext(request):
  context = None
  
  if checkUserAuth(request):
    context = Context({
    })
    if request.method == 'POST':
      form = UserAuthForm(request.POST)
    else:
      form = UserAuthForm(request.COOKIES)
    if form.is_valid():
      context.userLoginId = form.cleaned_data['userLoginId']
      context.userLoginAuth = form.cleaned_data['userLoginAuth']
    
    context.user = getUserByUserId(context.userLoginId)
    context.userLoginImg = tools.getUserImgUrl(context.user.email, 20)
    context.userLoginImg120 = tools.getUserImgUrl(context.user.email, 120)
    context.userUID = context.user.uid
  return context;

def delUserAuth(request):
  form = UserAuthForm();
  if request.method == 'POST':
    form = UserAuthForm(request.POST)
  else:
    form = UserAuthForm(request.COOKIES)
  if form.is_valid():
    userLoginId = form.cleaned_data['userLoginId']
    if tools.getSession(userLoginId):
      tools.delSession(userLoginId)
      return True;
      
  return False;

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

def checkIdAndEmail(userId, email):
  query = UserInfo.all()
  query.filter('userId = ', userId).filter('email = ', email)
  if query.count() == 0:
    return False;
  else:
    return True;
    
def setChangeFlag(userId, changeFlag):
  query = UserInfo.all()
  userInfos = query.filter('userId = ', userId)
  for userInfo in userInfos:
    userInfo.changeFlag = changeFlag
    userInfo.put()

def getUserByChangeFlag(changeFlag):
  query = UserInfo.all()
  user = query.filter('changeFlag = ', changeFlag).get()
    
  return user

def getUserByUserId(userId):
  query = UserInfo.all()
  user = query.filter('userId = ', userId).get()
    
  return user
