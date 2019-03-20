from django import forms
from user.models import Group
class LoginForm(forms.Form):
    username = forms.CharField(required=True,error_messages={'required':"用户名必填"})
    password = forms.CharField(required=True,error_messages={'required':"密码必填"})

class GroupForm(forms.ModelForm):
    class Meta:
        model=Group
        fields=['name','desc']