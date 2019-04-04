from django.http import JsonResponse
from django.views.generic.base import View,TemplateView
from django.shortcuts import render, get_object_or_404
from blog.models import Tag

from utils.mixin import AdminLoginRequiredMixin,BreadMixin

class TagView(AdminLoginRequiredMixin,BreadMixin,TemplateView):
    template_name = 'admin/tag/tag.html'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context['tags']=Tag.objects.all()
        return context


class TagCreateView(AdminLoginRequiredMixin,View):
    def get(self,request):
        return render(request,'admin/tag/tag_create.html')

    def post(self,request):
        res=dict(result=False)
        if request.POST['name']:
            name = request.POST['name']
            tag = Tag.objects.create(name=name)
            tag.save()
            res['result']=True
        return JsonResponse(res)


class TagUpdateView(AdminLoginRequiredMixin,View):
    def get(self,request):
        if 'id' in request.GET and request.GET['id']:
            tag = get_object_or_404(Tag,pk=int(request.GET['id']))
            ret=dict(tag=tag)
            return render(request,'admin/tag/tag_update.html',ret)

    def post(self,request):
        ret=dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            tag = get_object_or_404(Tag,pk=int(request.POST['id']))
            tag.name = request.POST.get('name')
            tag.save()
            ret['result']=True
        return JsonResponse(ret)


class TagDeleteView(AdminLoginRequiredMixin,View):
    def post(self,request):
        ret = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            tag = get_object_or_404(Tag,pk=int(request.POST['id']))
            tag.delete()
            ret['result']=True
            return JsonResponse(ret)