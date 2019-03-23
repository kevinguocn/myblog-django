from django.urls import path

from . import views,views_group,views_user,views_menu,views_role
app_name = 'admin'

urlpatterns=[
    #角色管理
    path("basic/role/",views_role.RoleIndexView.as_view(),name="role_index"),
    path("basic/role/create/",views_role.RoleCreateView.as_view(),name="role_create"),
    path("basic/role/list/",views_role.RoleListView.as_view(),name="role_list"),
    path("basic/role/update/",views_role.RoleUpdateView.as_view(),name="role_update"),
    path("basic/role/delete/",views_role.RoleDeleteView.as_view(),name="role_delete"),
    path("basic/role/role2user/",views_role.Role2User.as_view(),name="role_2user"),
    path("basic/role/role2menu/",views_role.Role2MenuView.as_view(),name="role_2menu"),
    path("basic/role/role2menu_list/",views_role.Role2MenuListView.as_view(),name="role_2menu_list"),
    #菜单管理
    path('basic/menu/create/',views_menu.MenuCreateView.as_view(),name='menu_create'),
    path('basic/menu/update/',views_menu.MenuUpdateView.as_view(),name='menu_update'),
    path('basic/menu/',views_menu.MenuListView.as_view(),name='menu_list'),
    #组管理
    path('basic/group/',views_group.GroupIndexView.as_view(),name='group_index'),
    path('basic/group/create/',views_group.GroupCreateView.as_view(), name='group_create'),
    path('basic/group/list/',views_group.GroupListView.as_view(), name='group_list'),
    path('basic/group/delete/',views_group.GroupDeleteView.as_view(), name='group_delete'),
    path('basic/group/add_user/',views_group.Group2UserView.as_view(), name='group_to_user'),
    #用户管理
    path('basic/user/',views_user.UserIndexView.as_view(),name='user_index'),
    path('basic/user/list/',views_user.UserListView.as_view(),name='user_list'),
    path('basic/user/create/',views_user.UserCreateView.as_view(),name='user_create'),
    path('basic/user/detail/',views_user.UserDetailView.as_view(),name='user_detail'),
    path('basic/user/update/',views_user.UserUpdateView.as_view(),name='user_update'),
    path('basic/user/redopwd/',views_user.UserPasswordRedoView.as_view(),name='user_redopassword'),
    path('basic/user/active/',views_user.UserActiveView.as_view(),name='user_active'),
    path('basic/user/unable/',views_user.UserUnableView.as_view(),name='user_unable'),
    #Admin 首页
    path('', views.AdminIndexView.as_view(), name='index')
]