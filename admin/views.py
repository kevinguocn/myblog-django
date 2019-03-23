from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import render
from mixin import AdminLoginRequiredMixin,BreadMixin
from django.views.generic.base import View,TemplateView


from .form import LoginForm
# Create your views here.
User = get_user_model()
class AdminIndexView(AdminLoginRequiredMixin,View):
    def get(self,request):
        user_num = User.objects.count()
        ret = dict(user_num=user_num)
        return  render(request,'admin/index.html',ret)