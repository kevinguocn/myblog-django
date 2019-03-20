from django.urls import path
from . import views,views_group
app_name = 'admin'

urlpatterns=[
    #组管理
    path('basic/group/',views_group.GroupIndexView.as_view(),name='group_index'),
    path('basic/group/create/',views_group.GroupCreateView.as_view(), name='group_create'),
    #Admin 首页
    path('', views.AdminIndexView.as_view(), name='index')
]