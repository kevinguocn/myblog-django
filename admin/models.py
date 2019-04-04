from django.db import models

# Create your models here.
from blog.models import Blog


class BackAdmin(models.Model):
    key = models.CharField(max_length=20,verbose_name='键')
    value = models.CharField(max_length=255,verbose_name='值')

    class Meta:
        db_table="tb_backadmin"
        verbose_name='后台表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.key


class Banner(models.Model):
    number = models.IntegerField()
    title = models.CharField(max_length=255)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    img = models.CharField(max_length=255)

    class Meta:
        db_table='tb_banner'
        verbose_name='banner表'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.title


class FriendLink(models.Model):
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=255)

    class Meta:
        db_table='tb_friendlink'
        verbose_name='友情链接'
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.name