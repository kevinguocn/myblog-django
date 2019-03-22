import re

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse
from django.urls import path
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View,TemplateView

from user.models import Role, Group
from .form import UserForm,UserUpdateForm

User = get_user_model()

from mixin import AdminLoginRequiredMixin
class UserIndexView(AdminLoginRequiredMixin,TemplateView):
    template_name = 'admin/user/user_index.html'


class UserListView(AdminLoginRequiredMixin,View):
    def get(self,request):
        fields = ['id','username','nickname','telephone','group__name','is_active','email']
        filters = dict()
        if 'select' in request.GET and request.GET['select']:
            filters['is_active'] =request.GET['select']
        ret = dict(data=list(User.objects.filter(**filters).values(*fields)))
        return JsonResponse(ret)

class UserCreateView(AdminLoginRequiredMixin,View):
    def get(self,request):
        roles = Role.objects.values()
        groups = Group.objects.values()
        ret = dict(
            roles = roles,
            groups = groups
        )
        return render(request,'admin/user/user_create.html',ret)

    def post(self,request):
        user_form = UserForm(request.POST)
        print(user_form)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.password = make_password('zxcmnb')
            new_user.save()
            user_form.save_m2m()
            ret = {"result":True}
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(user_form.errors)
            print(errors)
            user_create_form_errors = re.findall(pattern, errors)
            ret = {
                'status': False,
                'user_form_errors': user_create_form_errors[0]
            }
        return JsonResponse(ret)

class UserDetailView(AdminLoginRequiredMixin,View):
     def get(self,request):
         roles = Role.objects.values()
         groups = Group.objects.values()
         ret = dict(
             roles=roles,
             groups=groups
         )
         if 'id' in request.GET and request.GET['id']:
             user = get_object_or_404(User, pk=int(request.GET['id']))
             ret['update_user'] = user
             return render(request, 'admin/user/user_detail.html', ret)

class UserUpdateView(AdminLoginRequiredMixin,View):

    def post(self,request):
        ret = {"result":False}
        if 'id' in request.POST and request.POST['id']:
            user = get_object_or_404(User,pk=request.POST['id'])
        else:
            user = get_object_or_404(User,pk=request.user.id)

        user_update_form = UserUpdateForm(request.POST,instance=user)
        if user_update_form.is_valid():
            user_update_form.save()
            ret['result'] = True
        else:
            pattern = '<li>.*?<ul class=.*?><li>(.*?)</li>'
            errors = str(user_update_form.errors)
            user_update_form_errors = re.findall(pattern, errors)
            ret = {
                'status': False,
                'user_form_errors': user_update_form_errors[0]
            }
        return JsonResponse(ret)

class UserPasswordRedoView(AdminLoginRequiredMixin,View):
    def post(self,request):
        ret=dict(result=False)
        if request.user.is_superuser:
            if 'id' in request.POST and request.POST['id']:
                user = get_object_or_404(User, pk=int(request.POST['id']))
                print(user)
                if user is not request.user:
                    user.password = make_password('zxcmnb')
                    user.save()
                    ret['result'] = True
                else:
                    ret['msg']="不能为自己初始化密码"
        else:
            ret['msg'] = "无超级管理员权限"
        return JsonResponse(ret)

class UserActiveView(AdminLoginRequiredMixin,View):
    def post(self,request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int,request.POST['id'].split(','))
            users = User.objects.filter(id__in=id_list)
            print(users)
            for user in users:
                user.is_active = True
                user.save()
            ret['result'] = True
        return JsonResponse(ret)

class UserUnableView(AdminLoginRequiredMixin,View):
    def post(self,request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            id_list = map(int,request.POST['id'].split(','))
            users = User.objects.filter(id__in=id_list)
            for user in users:
                user.is_active = False
                user.save()
            ret['result'] = True
        return JsonResponse(ret)