# coding=UTF-8
from datetime import datetime
import hashlib
import random
from google.appengine.api import memcache

#defualt expiration time
timeout = 1800

def getAuthCode(sid, userId):
  """
  getAuthCode(userId, sid)
  get the hash value of the login user
  """
  dt = datetime.now()
  dtstr = dt.strftime("%Y-%m-%d %H:%M:%S")
  toHashStr = sid + ":" + userId + ":" + dtstr
  return hashlib.sha256(toHashStr).hexdigest()
  
def getUserSid(userId):
  """
  get a user's session id
  """
  sid = getSession(userId)
  if sid is None:
    ranFloat = random.random()
    sid = hashlib.sha256(userId + ":" + repr(ranFloat)).hexdigest()
    addToSession(userId, sid)
    return sid
  else:
    return sid    

def addToSession(key, value):
  """
    Add a key's value, expiration in time
  """
  oldValue = memcache.get(key)
  if oldValue is None:
    memcache.add(key, value, timeout)
  else:
    memcache.replace(key, value, timeout)

def delFromSession(key):
  """
  delete a key from session
  """
  memcache.delete(key)
  
def getSession(key):
  return memcache.get(key)
  
def addUserAuth(userId, sid, auth):
  addToSession(userId + ":" + sid, auth)
  
def addUserAuth(userId, sid, auth, time):
  addToSession(userId + ":" + sid, auth, time)
  
def getUserAuth(userId, sid):
  return getSession(userId + ":" + sid)
  
def delUserAuth(userId, sid):
  delFromSession(userId + ":" + sid)
