from blog.models import Tag
from admin.models import FriendLink


def side_context(request):
    tags = Tag.objects.all()
    friendlinks = FriendLink.objects.all()
    return {'tags':tags,
            'friendlinks':friendlinks
            }