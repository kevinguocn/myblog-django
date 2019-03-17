from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(required=True,error_messages={'required':"用户名必填"})
    password = forms.CharField(required=True,error_messages={'required':"密码必填"})
