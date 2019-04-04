from django.contrib.auth import get_user_model
from django.shortcuts import render

from blog.models import Blog
from utils.mixin import AdminLoginRequiredMixin
from django.views.generic.base import View

# Create your views here.
User = get_user_model()
class AdminIndexView(AdminLoginRequiredMixin,View):
    def get(self,request):
        user_num = User.objects.count()
        blog_num = Blog.objects.count()
        ret = dict(user_num=user_num,
                   blog_num=blog_num)
        return  render(request,'admin/index.html',ret)

