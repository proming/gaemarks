# coding=UTF-8
from django import forms

class LoginForm(forms.Form):
  userId=forms.CharField(label='用户名',max_length=20,required=True)
  passwd=forms.CharField(label='密码',max_length=64,required=True)

class UserInfoForm(forms.Form):
  userId=forms.CharField(label='用户名',max_length=20,required=True)
  passwd=forms.CharField(label='密码',max_length=64,required=True)
  email=forms.EmailField(label='邮箱',required=True)

class UserAuthForm(forms.Form):
  userId=forms.CharField(label='用户名',required=True)
  authCode=forms.CharField(label='授权码',required=True)
