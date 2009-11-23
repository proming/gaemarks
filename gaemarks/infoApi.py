# coding=UTF-8

from google.appengine.ext import db
from google.appengine.ext.db import GqlQuery
from google.appengine.api import users
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from models import UserInfo
from forms import UserInfoForm, ChangePasswdForm
import gaemarks.tools as tools
import gaemarks.userApi as userApi
from django.utils import simplejson as json

def updateInfo(request):
  reponse = dict()
  reponse.update(status = 0, msg = '录入信息错误，请重新录入！')
  if not userApi.checkUserAuth(request):
    reponse.update(msg = '请重新登录系统重试！')
    return HttpResponse(json.dumps(reponse),mimetype='application/json')
  
  msg = ''
  if request.method == 'POST':
    form = UserInfoForm(request.POST)
    if form.is_valid():
      if not userApi.authService(form.cleaned_data['userId'], form.cleaned_data['passwd']):
        msg = '密码不正确！'
      else:
        userInfo = userApi.getUserByUserId(form.cleaned_data['userId'])
        userInfo.email = form.cleaned_data['email']
        remarks = form.cleaned_data['remark']
        userInfo.remark = remarks
        userInfo.put();
        msg = '信息更新成功!'
        reponse.update(status = 1)
  if msg != '':
    reponse.update(msg = msg)
  return HttpResponse(json.dumps(reponse),mimetype='application/json')

def changePasswd(request):
  reponse = dict()
  reponse.update(status = 0, msg = '录入信息错误，请重新录入！')
  if not userApi.checkUserAuth(request):
    reponse.update(msg = '请重新登录系统重试！')
    return HttpResponse(json.dumps(reponse),mimetype='application/json')
    
  msg = ''
  if request.method == 'POST':
    form = ChangePasswdForm(request.POST)
    if form.is_valid():
      if not userApi.authService(form.cleaned_data['userId'], form.cleaned_data['passwd']):
        msg = '密码不正确！'
      else:
        userInfo = userApi.getUserByUserId(form.cleaned_data['userId'])
        userInfo.passwd = form.cleaned_data['repasswd']
        userInfo.put();
        msg = '修改密码成功!'
        reponse.update(status = 1)
  if msg != '':
    reponse.update(msg = msg)
  return HttpResponse(json.dumps(reponse),mimetype='application/json')

