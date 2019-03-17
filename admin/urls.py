from django.urls import path
from . import views
app_name = 'admin'

urlpatterns=[
#admin index
    path('',views.AdminIndexView.as_view(),name='index')
]