# coding=UTF-8
from google.appengine.ext import db

class UserInfo(db.Model):
  uid=db.IntegerProperty()
  userId=db.StringProperty()
  passwd=db.StringProperty()
  email=db.EmailProperty()
  regtime=db.DateTimeProperty(auto_now_add=True)
  changeFlag=db.StringProperty()
  updateCount=db.IntegerProperty(default=0)
  updateTime=db.DateTimeProperty()
  remark=db.TextProperty(default='')
  
  def create(self):
    userCount = UserCount.all().get()
    uidDB = 1
    if userCount:
      uidDB = userCount.uid + 1
      userCount.uid = uidDB
      userCount.put()
    else:
      userCount = UserCount()
      userCount.uid = uidDB
      userCount.put()
      
    self.uid = uidDB
    self.put()
    
class UserCount(db.Model):
  uid=db.IntegerProperty()

