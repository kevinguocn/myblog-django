from django.views.generic.base import View, TemplateView
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from mixin import AdminLoginRequiredMixin, BreadMixin
from user.models import Menu
from admin.form import MenuForm


class MenuCreateView(AdminLoginRequiredMixin, View):
    def get(self, request):
        ret = dict(menu_all=Menu.objects.all())
        return render(request, 'admin/menu/menu_create.html', ret)

    def post(self, request):
        ret = dict(result=False)
        menu = Menu()
        menu_form = MenuForm(request.POST, instance=menu)
        if menu_form.is_valid():
            menu_form.save()
            ret['result']=True
        return JsonResponse(ret)

class MenuListView(AdminLoginRequiredMixin,BreadMixin,TemplateView):
    template_name = 'admin/menu/menu.html'
    extra_context = dict(menu_all=Menu.objects.all())


class MenuUpdateView(AdminLoginRequiredMixin,View):
    def get(self, request):
        if "id" in request.GET and request.GET['id']:
            menu = get_object_or_404(Menu, pk=int(request.GET['id']))
            menu_all = Menu.objects.exclude(pk=int(request.GET['id'])).all()
            ret = dict(menu=menu, menu_all=menu_all)
            return render(request, 'admin/menu/menu_update.html', ret)


    def post(self,request):
        ret=dict(result=False)
        if 'id' in request.POST and request.POST['id']:
            menu = get_object_or_404(Menu,pk=int(request.POST['id']))
            menu_form = MenuForm(request.POST,instance=menu)
            if menu_form.is_valid():
                menu_form.save()
                print(menu_form.errors)
                ret['result']=True
        return JsonResponse(ret)

