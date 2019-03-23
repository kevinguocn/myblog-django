import re

from django import forms
from django.contrib.auth import get_user_model

from user.models import Group,Menu,Role
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
        fields=['username','nickname','email','telephone','group','gender','roles','birthday','is_active']


    def clean(self):
        cleaned_data = super(UserForm,self).clean()
        username = cleaned_data.get('username')
        telephone = cleaned_data.get('telephone')
        email = cleaned_data.get('email')
        if User.objects.filter(username=username).count():
            raise forms.ValidationError("用户名{}存在".format(username))
        if User.objects.filter(telephone=telephone).count():
            raise forms.ValidationError("手机号{}存在".format(telephone))
        if User.objects.filter(email=email).count():
            raise forms.ValidationError("邮箱{}重复".format(email))
        REGEX_MOBILE = "^1[3578]\d{9}$|^147\d{8}$|^176\d{8}$"
        if telephone and (not re.match(REGEX_MOBILE, telephone)):
            raise forms.ValidationError("手机号码非法")

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['username','nickname','email','telephone','group','gender','roles','birthday','is_active']


class MenuForm(forms.ModelForm):

    class Meta:
        model=Menu
        fields="__all__"


class RoleForm(forms.ModelForm):

    class Meta:
        model=Role
        fields="__all__"