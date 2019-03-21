from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.urls import path
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View,TemplateView
User = get_user_model()

from mixin import AdminLoginRequiredMixin
class UserIndexView(AdminLoginRequiredMixin,TemplateView):
    template_name = 'admin/user/user_index.html'


class UserListView(AdminLoginRequiredMixin,View):
    def get(self,request):
        fields = ['id','username','nickname','telephone','group__name','is_active','email']
        ret = dict(data=list(User.objects.values(*fields)))
        return JsonResponse(ret)

class UserCreateView(AdminLoginRequiredMixin,View):
    def get(self,request):
        if 'id' in request.GET and request.GET['id']:
            user = get_object_or_404(User,pk=int(request.GET['id']))
        else:
            user = User()
