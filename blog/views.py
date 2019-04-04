from django.shortcuts import render, get_object_or_404
from utils.mixin import AdminLoginRequiredMixin
# Create your views here.
from django.views.generic.base import View

from blog.models import Blog, Tag, ReadNum
from utils import readnum

class BlogDetailView(View):
    """
    博客详情页
    """
    def get(self,request,blog_id):
        blog = get_object_or_404(Blog,pk=blog_id)
        pre_blog = Blog.objects.filter(create_time__gt=blog.create_time).last()
        next_blog = Blog.objects.filter(create_time__lt=blog.create_time).first()
        key = readnum.read_statistics_once_read(request,blog)
        read_num = readnum.get_read_num(blog)
        context = dict(blog=blog,
                       pre_blog=pre_blog,
                       next_blog=next_blog)
        response = render(request,'blog/blog_detail.html',context)
        response.set_cookie(key,'true')
        return response

class BlogListView(View):
    """
    博客列表页
    """
    def get(self,request):
        fields = {}
        context = {}
        if 'tag' in request.GET and request.GET['tag']:
            fields.update({"tag":request.GET['tag']})
            context.update({"tag":Tag.objects.filter(pk=int(request.GET['tag'])).first()})
        if 'page' in request.GET and request.GET['page']:
            page = request.GET['page']
        else:
            page=1
        blogs = Blog.objects.filter(**fields).all()
        context['blogs']=blogs
        return render(request,'blog/blog_index.html',context)

