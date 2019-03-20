from django.http import JsonResponse
from django.views.generic.base import View, TemplateView
from django.shortcuts import render, get_object_or_404

from mixin import AdminLoginRequiredMixin
from user.models import Group
from .form import GroupForm

class GroupIndexView(AdminLoginRequiredMixin,TemplateView):
    template_name = 'admin/group/group_index.html'

class GroupCreateView(AdminLoginRequiredMixin,View):
    def get(self,request):
        ret={}
        if 'id' in request.GET and request.GET['id']:
            id = request.GET['id']
            group = get_object_or_404(Group,pk=int(id))
            ret = dict(group = group)
        return render(request,'admin/group/group_create.html',ret)

    def post(self,request):
        res = dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            group = get_object_or_404(Group,pk=int(request.POST['id']))
        else:
            group = Group()
        group_form = GroupForm(request.POST,instance=group)
        if group_form.is_valid():
            group_form.save()
            res['result']=True
        print(res)
        print(group_form.errors)
        return JsonResponse(res)


class GroupListView(AdminLoginRequiredMixin,View):
    def get(self,request):
        fields = ['id','name','desc']
        ret = dict(data = list(Group.objects.values(*fields)))
        return JsonResponse(ret)

class GroupDeleteView(AdminLoginRequiredMixin,View):
    def post(self,request):
        ret=dict(result=False)
        if "id" in request.POST and request.POST['id']:
            id_list = map(int,request.POST['id'].split(','))
            Group.objects.filter(id__in=id_list).delete()
            ret['result']=True
        return JsonResponse(ret)