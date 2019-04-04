

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone

User = get_user_model()
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=20,verbose_name="标签名",unique=True)

    class Meta:
        db_table='tb_tag'
        verbose_name="标签"
        verbose_name_plural=verbose_name
        ordering=['-id']

    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=20,verbose_name='标题')
    author = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='作者')
    tag = models.ForeignKey(Tag,on_delete=models.DO_NOTHING,verbose_name='标签')
    content =  models.TextField(verbose_name="内容")
    create_time = models.DateTimeField(auto_now_add=True,verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True,verbose_name="修改时间")

    class Meta:
        db_table="tb_blog"
        verbose_name="博客"
        verbose_name_plural=verbose_name
        ordering=['-update_time','-id']

    def __str__(self):
        return self.title

    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)
            readnum=ReadNum.objects.filter(content_type=ct,object_id=self.pk).first()
            return readnum.read_num
        except Exception as e:
            return 0


class ReadNum(models.Model):
    read_num = models.IntegerField(default=0)
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()

    content_object = GenericForeignKey('content_type','object_id')

    class Meta:
        db_table='tb_read_num'
        verbose_name='阅读计数'
        verbose_name_plural=verbose_name
        ordering=['-read_num']


class ReadDetail(models.Model):
    """
    根据日期计数的模型类
    继承model.Model
    """
    read_num = models.IntegerField(default=0)
    date = models.DateField(default=timezone.now)

    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')

    class Meta:
        verbose_name="阅读记录"
        verbose_name_plural=verbose_name
        db_table='tb_readdetail'
        ordering=['-date']