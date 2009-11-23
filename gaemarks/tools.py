# coding=UTF-8
from datetime import datetime
import urllib, hashlib, random
from google.appengine.api import memcache
from google.appengine.api import mail

#defualt expiration time
timeout = 1800

def getAuthCode(userId):
  """
  getAuthCode(userId, sid)
  get the hash value of the login user
  """
  dt = datetime.now()
  dtstr = dt.strftime("%Y-%m-%d %H:%M:%S")
  randomNum = random.random()
  toHashStr = userId + ":" + dtstr + ":" + str(randomNum)
  return hashlib.sha256(toHashStr).hexdigest() 

def addSession(key, value):
  """
    Add a key's value, expiration in time
  """
  oldValue = memcache.get(key)
  if oldValue is None:
    memcache.add(key, value, timeout)
  else:
    memcache.replace(key, value, timeout)

def delSession(key):
  """
  delete a key from session
  """
  memcache.delete(key)
  
def getSession(key):
  return memcache.get(key)
  
def getUserImgUrl(email, size):
  default = "http://gaemarks.appspot.com/image/userimg" + str(size) + ".png"

  # construct the url
  gravatar_url = "http://www.gravatar.com/avatar.php?"
  gravatar_url += urllib.urlencode({'gravatar_id':hashlib.md5(email).hexdigest(), 
	  'default':default, 'size':str(size)})
  return gravatar_url

def sendEmail(userId, email):
  dt = datetime.now()
  dtstr = dt.strftime("%Y-%m-%d %H:%M:%S")
  
  randomNum = random.random()
  toHashStr = userId + ":" + dtstr + ":" + email + ":" + str(randomNum)
  changeFlag = hashlib.sha256(toHashStr).hexdigest()
  
  url = u'http://gaemarks.appspot.com/resetPasswd/' + changeFlag + u''
  
  body = u"""
尊敬的%s：

您好！

根据您于 [%s] 提交的请求，本邮件将引导您重新设置 [%s] 的GAEMarks帐号密码。
如果您确认本次“重新设置密码”的请求是您自己提交的，请点这里完成重设操作。
复制以下链接，粘贴到您浏览器的地址栏内，然后按“回车”键打开重设密码：

%s

如果您在以上时间点没有提交过“重新设置密码”的请求，则有可能是有恶意用户正在试图窃取您的帐号！强烈建议您尽快登录GAEMarks修改您的密码。

(本邮件为系统自动发出，请勿回复。)

-------------
感谢您使用GAEMarks，有任何问题您都可以发送邮件给%s！

GAEMarks Service Group"""
  message = mail.EmailMessage()
  message.sender = "longming.fu@gmail.com"
  message.subject="GAEMarks密码重设邮件（请勿回复）"
  message.to = email 
  message.body = body % (userId, dtstr, userId, url, u'promingx@gmal.com')
  addSession(userId+'1', message.body)
  message.send()
  return changeFlag;
