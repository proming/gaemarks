# coding=UTF-8
from google.appengine.ext import db

class UserInfo(db.Model):
  userId=db.StringProperty()
  passwd=db.StringProperty()
  email=db.EmailProperty()
  regtime=db.DateTimeProperty(auto_now_add=True)
  changeFlag=db.StringProperty()
  updateCount=db.IntegerProperty(default=0)
  updateTime=db.DateTimeProperty()
  remark=db.StringProperty()


