from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.generic.base import View, TemplateView
from django.shortcuts import render, get_object_or_404

from mixin import AdminLoginRequiredMixin
from user.models import Group
from .form import GroupForm

User = get_user_model()



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


class Group2UserView(AdminLoginRequiredMixin,View):
    def get(self,request):
        if 'id' in request.GET and request.GET['id']:
            group = get_object_or_404(Group,pk=int(request.GET['id']))
            #查出所有关联此组的用户
            added_users = group.user_set.all()
            #查出所有用户的信息
            all_users = User.objects.all()
            #未添加的用户
            un_added_users = set(all_users).difference(added_users)
            ret = dict(group = group,all_users=all_users,un_added_users=un_added_users,added_users=added_users)
            print(ret)
            return render(request,'admin/group/group_user.html',ret)

    def post(self,request):
        res = dict(result = False)
        id_list = None
        group = get_object_or_404(Group,pk=int(request.POST['id']))
        if 'to' in request.POST and request.POST.getlist("to",[]):
            id_list = map(int,request.POST.getlist("to",[]))
        group.user_set.clear()
        if id_list:
            for user in User.objects.filter(id__in=id_list).all():
                group.user_set.add(user)
        res['result']=True
        return JsonResponse(res)
