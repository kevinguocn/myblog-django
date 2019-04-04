from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Menu(models.Model):
    """
    菜单
    """
    name = models.CharField(max_length=30, unique=True, verbose_name="菜单名")  # unique=True, 这个字段在表中必须有唯一值.
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, verbose_name="父菜单")
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="图标")
    code = models.CharField(max_length=50, null=True, blank=True, verbose_name="编码")
    url = models.CharField(max_length=128, unique=True, null=True, blank=True)
    number = models.FloatField(null=True, blank=True, verbose_name="编号")

    def __str__(self):
        return self.name

    class Meta:
        db_table='tb_menu'
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering=['number']

    @classmethod
    def get_menu_by_request_url(cls, url):
        try:
            return dict(menu=Menu.objects.get(url=url))
        except:
            return None

class Role(models.Model):
    name = models.CharField(max_length=20,verbose_name='角色名')
    permissions = models.ManyToManyField(Menu, blank=True, verbose_name="URL授权")
    desc = models.CharField(max_length=20,verbose_name='角色描述')
    class Meta:
        db_table='tb_role'

    def __str__(self):
        return self.name

class Group(models.Model):
    '''
    用户组
    '''
    name = models.CharField(max_length=120,unique=True,verbose_name='用户组')
    desc = models.CharField(max_length=50, blank=True, null=True, verbose_name="描述")

    class Meta:
        db_table='tb_group'
        verbose_name='用户组'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class User(AbstractUser):
    """
    用户
    """
    telephone = models.CharField(max_length=11,unique=True,verbose_name='手机号',blank=True,null=True)
    nickname = models.CharField(max_length=20,verbose_name='昵称',blank=True,null=True)
    birthday = models.DateField(default="2000-1-1",blank=True,null=True)
    email_active = models.BooleanField(default=0,verbose_name='email激活状态')
    gender = models.CharField(max_length=10,choices=(("male","男"),("female","女")),default="male",verbose_name='性别',blank=True)
    image = models.ImageField(upload_to="image/%Y/%m",default="image/default.jpg",max_length=120,null=True,blank=True)
    group = models.ForeignKey(Group,null=True,blank=True,on_delete=models.SET_NULL,verbose_name='用户组')
    roles = models.ManyToManyField(Role,verbose_name='角色',blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='tb_user'
        verbose_name='用户'
        verbose_name_plural=verbose_name
        ordering=['-id']

    def __str__(self):
        return self.username

    def has_per_in_admin(self):
        return True
