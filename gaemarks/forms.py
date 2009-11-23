# coding=UTF-8
from django import forms

class LoginForm(forms.Form):
  userId=forms.CharField(label='用户名',max_length=20,required=True)
  passwd=forms.CharField(label='密码',max_length=64,required=True)

class UserInfoForm(forms.Form):
  userId=forms.CharField(label='用户名',max_length=20,required=True)
  passwd=forms.CharField(label='密码',max_length=64,required=True)
  email=forms.EmailField(label='邮箱',required=True)
  remark=forms.CharField(label='备注',widget=forms.Textarea)

class UserAuthForm(forms.Form):
  userLoginId=forms.CharField(label='用户名',required=True)
  userLoginAuth=forms.CharField(label='授权码',required=True)
  
class ForgotRequestForm(forms.Form):
  userId=forms.CharField(label='用户名',required=True)
  email=forms.CharField(label='密码',required=True)

class PasswdResetForm(forms.Form):
  userId=forms.CharField(label='用户名',max_length=20,required=True)
  passwd=forms.CharField(label='密码',max_length=64,required=True)
  changeFlag=forms.CharField(label='修改标识',required=True)
  
class ChangePasswdForm(forms.Form):
  userId=forms.CharField(label='用户名',max_length=20,required=True)
  passwd=forms.CharField(label='密码',max_length=64,required=True)
  repasswd=forms.CharField(label='密码',max_length=64,required=True)

