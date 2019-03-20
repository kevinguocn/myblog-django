from django.http import JsonResponse
from django.views.generic.base import View, TemplateView
from django.shortcuts import render

from mixin import AdminLoginRequiredMixin
from user.models import Group
from .form import GroupForm

class GroupIndexView(AdminLoginRequiredMixin,TemplateView):
    template_name = 'admin/group/group_index.html'

class GroupCreateView(AdminLoginRequiredMixin,View):
    def get(self,request):
        ret = dict(groups = Group.objects.all())
        return render(request,'admin/group/group_create.html',ret)

    def post(self,request):
        res = dict(result=False)
        group = Group()
        group_form = GroupForm(request.POST,instance=group)
        if group_form.is_valid():
            group_form.save()
            res['result']=True

        return JsonResponse(res)