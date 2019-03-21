from django import forms
from django.contrib.auth import get_user_model

from user.models import Group
User=get_user_model()
class LoginForm(forms.Form):
    username = forms.CharField(required=True,error_messages={'required':"用户名必填"})
    password = forms.CharField(required=True,error_messages={'required':"密码必填"})

class GroupForm(forms.ModelForm):
    class Meta:
        model=Group
        fields=['name','desc']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['username','nickname','email','telephone','group__id']