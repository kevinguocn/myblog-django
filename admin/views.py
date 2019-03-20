from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from mixin import AdminLoginRequiredMixin
from django.views.generic.base import View,TemplateView


from .form import LoginForm
# Create your views here.

class AdminIndexView(AdminLoginRequiredMixin,View):
    def get(self,request):
        return  render(request,'admin/index.html')


class AdminGroupView(AdminLoginRequiredMixin,TemplateView):
    template_name = 'admin/group/group_index.html'