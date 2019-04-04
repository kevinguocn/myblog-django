from blog.models import Blog
from admin.models import BackAdmin

def get_top_blog():
    blog_id = BackAdmin.objects.filter(key="top_blog").first()
    if blog_id:
        blog = Blog.objects.filter(pk=int(blog_id.value)).first()

    else:
        blog = Blog.objects.first()
    return blog