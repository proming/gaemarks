# coding=UTF-8

from google.appengine.ext import db
from google.appengine.ext.db import GqlQuery
from google.appengine.api import users
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, Context
from gaemarks.models import UserInfo
from forms import LoginForm, UserInfoForm, UserAuthForm
import gaemarks.tools as tools
import gaemarks.userApi as userApi

def siteView(request):
  context = userApi.getUserAuthContext(request)
  if not context:
    context = Context({
    })
  
  template = loader.get_template('html/comingsoon.html')
  return HttpResponse(template.render(context))

