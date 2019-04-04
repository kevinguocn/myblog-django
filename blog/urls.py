from django.urls import path
from . import views
app_name = 'blog'
urlpatterns = [
    path("<int:blog_id>/",views.BlogDetailView.as_view(),name="blog_detail"),
    path("list/",views.BlogListView.as_view(),name="blog_list")
]