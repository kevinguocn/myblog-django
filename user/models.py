from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=120,unique=True,verbose_name='用户组')

    class Meta:
        db_table='tb_group'
        verbose_name='用户组'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name

class User(AbstractUser):
    '''

    '''
    nickname = models.CharField(max_length=20,verbose_name='昵称')
    email_active = models.BooleanField(default=0,verbose_name='email激活状态')
    gender = models.CharField(max_length=10,choices=(("male","男"),("female","女")),default="male",verbose_name='性别')
    image = models.ImageField(upload_to="image/%Y/%m",default="image/default.jpg",max_length=120,null=True,blank=True)
    group = models.ForeignKey(Group,null=True,blank=True,on_delete=models.SET_NULL,verbose_name='用户组')
    create_time = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='tb_user'
        verbose_name='用户'
        verbose_name_plural=verbose_name
        ordering=['-id']

    def __str__(self):
        return self.username
