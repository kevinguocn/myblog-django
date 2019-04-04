from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from admin.form import LoginForm
from admin.models import Banner
from blog.models import Blog

from utils.index import get_top_blog

class IndexView(View):
    def get(self,request):
        new_blogs = Blog.objects.all()[:5]
        banners = Banner.objects.all()[:4]

        context = dict(new_blogs=new_blogs,
                       banners=banners,
                       banners_num = range(len(banners)),
                       top_blog = get_top_blog())
        return render(request,'index.html',context)


class LoginView(View):
    def get(self,request):
        redirect_to = request.GET.get('next', '/')
        context = dict(redirect_to=redirect_to)
        if request.user.is_authenticated:
            return HttpResponseRedirect(redirect_to)
        else:
            return render(request,'admin/user/login.html',context)

    def post(self,request):
        redirect_to = request.GET.get('next','/')
        login_form = LoginForm(request.POST)
        ret = dict(login_form=login_form)
        if login_form.is_valid():
            user_name = login_form.cleaned_data.get('username')
            pass_word = login_form.cleaned_data.get('password')
            user = authenticate(username = user_name,password=pass_word)
            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(redirect_to)
                else:
                    ret['msg']='用户未激活'
            else:
                ret['msg']='登陆出错'
        else:
            ret['msg']='用户名密码不可为空'
        return render(request,'admin/user/login.html',ret)


class LogoutView(View):
    def get(self,request):
        redirect_to = request.GET.get('next','/')
        logout(request)
        return HttpResponseRedirect(redirect_to)