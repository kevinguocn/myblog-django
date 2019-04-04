from django.contrib.contenttypes.models import ContentType
from django.utils import timezone

from blog.models import ReadNum, ReadDetail


def read_statistics_once_read(request,obj):
    """
    阅读+1
    :param request: 请求实体
    :param obj: 增加对象的实体
    :return:
    """
    ct = ContentType.objects.get_for_model(obj)
    key = "{}_{}_read".format(ct.model,obj.pk)
    if not request.COOKIES.get(key):
        readnum,created = ReadNum.objects.get_or_create(content_type=ct,object_id=obj.pk)
        readnum.read_num += 1
        readnum.save()

        #当前的阅读数+1
        date = timezone.now().date()
        readtail,created = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk, date=date)
        readtail.read_num += 1
        readtail.save()
    return key


def get_read_num(obj):
    ct = ContentType.objects.get_for_model(obj)
    try:
        read_num = ReadDetail.objects.filter(content_type=ct,object_id=obj.pk).first()
    except Exception:
        return 0
    return read_num.read_num