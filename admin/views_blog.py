import datetime

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View,TemplateView

from admin.form import BlogForm
from blog.models import Blog, Tag

from utils.mixin import AdminLoginRequiredMixin,BreadMixin
User = get_user_model()
class AdminBlogIndexView(AdminLoginRequiredMixin,View):
    def get(self,request):
        return render(request,'admin/blog_index.html')


class AdminBlogView(AdminLoginRequiredMixin,BreadMixin,TemplateView):
    template_name = "admin/blog/blog.html"


class AdminBlogListView(AdminLoginRequiredMixin,View):
    def get(self,request):
        fields = ['id','title','author__nickname',"create_time","update_time","tag__name"]
        ret = dict(data = list(Blog.objects.values(*fields)))
        return JsonResponse(ret)


class AdminBlogDeleteView(AdminLoginRequiredMixin,View):
    def post(self,request):
        ret=dict(result=False)
        if "id" in request.POST and request.POST['id']:
            id_list = map(int,request.POST['id'].split(","))
            blogs = Blog.objects.filter(id__in=id_list)
            for blog in blogs:
                blog.delete()
            ret['result']=True
        return JsonResponse(ret)

class AdminBlogCreateView(AdminLoginRequiredMixin,View):

    def get(self,request):
        ret = dict()
        ret['tags']=Tag.objects.all()
        return render(request,'admin/blog/blog_create.html',ret)

    def post(self,request):
        ret=dict(result = False)
        blog = Blog()
        blog_form = BlogForm(request.POST,instance=blog)
        if blog_form.is_valid():
            new_blog = blog_form.save(commit=False)
            new_blog.author = request.user
            new_blog.save()
            ret['result']=True
        else:
            ret['msg']=blog_form.errors
        return JsonResponse(ret)


class AdminBlogUpdateView(AdminLoginRequiredMixin,View):
    def get(self,request):
        if "id" in request.GET and request.GET['id']:
            blog = get_object_or_404(Blog,pk=int(request.GET['id']))
            ret = dict(blog=blog,
                       tags = Tag.objects.all())

            return render(request,'admin/blog/blog_update.html',ret)

    def post(self, request):
        ret = dict(result=False)
        if "id" in request.POST and request.POST['id']:
            blog = get_object_or_404(Blog, pk=int(request.POST['id']))
            if request.user == blog.author:
                blog_form = BlogForm(request.POST, instance=blog)
                if blog_form.is_valid():
                    update_blog=blog_form.save(commit=False)
                    update_blog.update_time = datetime.time()
                    update_blog.save()
                    ret['result'] = True
                else:
                    ret['msg'] = blog_form.errors
        return JsonResponse(ret)
