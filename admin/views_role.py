import json

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View, TemplateView

from utils.mixin import AdminLoginRequiredMixin, BreadMixin
from user.models import Role, Menu
from .form import RoleForm

User = get_user_model()


class RoleIndexView(AdminLoginRequiredMixin, BreadMixin,TemplateView):
    template_name = "admin/role/role.html"


class RoleCreateView(AdminLoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'admin/role/role_create.html')

    def post(self, request):
        ret = dict(result=False)
        role = Role()
        role_form = RoleForm(request.POST, instance=role)
        if role_form.is_valid():
            role_form.save()
            ret['result'] = True
        return JsonResponse(ret)


class RoleListView(AdminLoginRequiredMixin, View):
    def get(self, request):
        ret = dict(data=list(Role.objects.values()))
        return JsonResponse(ret)


class RoleUpdateView(AdminLoginRequiredMixin, View):
    def get(self, request):
        if "id" in request.GET and request.GET['id']:
            role = get_object_or_404(Role, pk=int(request.GET['id']))
            return render(request, 'admin/role/role_update.html', {"role": role})

    def post(self, request):
        if "id" in request.POST and request.POST['id']:
            ret = dict(result=False)
            role = get_object_or_404(Role, pk=int(request.POST['id']))
            role_form = RoleForm(request.POST, instance=role)
            if role_form.is_valid():
                role_form.save()
                ret['result'] = True
            else:
                ret['msg'] = role_form.errors
            return JsonResponse(ret)


class RoleDeleteView(AdminLoginRequiredMixin, View):

    def post(self, request):
        ret = dict(result=False)
        if "id" in request.POST and request.POST['id']:
            id_list = map(int, request.POST['id'].split(','))
            roles = Role.objects.filter(id__in=id_list)
            if id_list:
                for role in roles:
                    role.delete()
                ret['result'] = True
        return JsonResponse(ret)


class Role2User(AdminLoginRequiredMixin, View):
    def get(self, request):
        if 'id' in request.GET and request.GET['id']:
            role = get_object_or_404(Role, pk=int(request.GET['id']))
            all_user = User.objects.all()
            added_users = role.user_set.all()
            unadded_users = set(all_user).difference(added_users)
            ret = dict(
                role=role,
                unadded_users=unadded_users,
                added_users=added_users
            )
            return render(request, 'admin/role/role_2user.html', ret)
    def post(self,request):
        res = dict(result = False)
        id_list = None
        role = get_object_or_404(Role,pk=int(request.POST['id']))
        if 'to' in request.POST and request.POST.getlist("to",[]):
            id_list = map(int,request.POST.getlist("to",[]))
        role.user_set.clear()
        if id_list:
            for user in User.objects.filter(id__in=id_list).all():
                role.user_set.add(user)
            res['result']=True
        return JsonResponse(res)


class Role2MenuView(AdminLoginRequiredMixin,View):
    """
    角色绑定菜单
    """
    def get(self,request):
        if 'id' in request.GET and request.GET['id']:
            role = get_object_or_404(Role,pk=int(request.GET['id']))
            ret = dict(role=role)
            return render(request,'admin/role/role_role2menu.html',ret)

    def post(self,request):
        ret = dict(result=False)
        role = get_object_or_404(Role,pk=int(request.POST['id']))
        tree = json.loads(self.request.POST['tree'])
        #清除所有的信息
        role.permissions.clear()
        for menu in tree:
            if menu['checked'] is True:
                menu_checked = get_object_or_404(Menu,pk=menu['id'])
                role.permissions.add(menu_checked)
        ret['result']=True
        return JsonResponse(ret)

class Role2MenuListView(AdminLoginRequiredMixin,View):
    """
    zTree 在生成菜单树状结构时，会通过该接口获取菜单列表数据
    """
    def get(self,request):
        fields = ['id','name','parent']
        if 'id' in request.GET and request.GET['id']:
            role = Role.objects.get(id=request.GET['id'])
            role_menu = role.permissions.values(*fields)
            ret = dict(data=list(role_menu))
        else:
            menus = Menu.objects.all()
            ret = dict(data=list(menus.values(*fields)))
        return JsonResponse(ret)