import re

from django.contrib.auth.decorators import login_required

from user.models import Menu


class AdminLoginRequiredMixin(object):
    @classmethod
    def as_view(cls,**init_kwargs):
        view = super(AdminLoginRequiredMixin, cls).as_view(*init_kwargs)
        return login_required(view)


class BreadMixin(object):
    def get_context_data(self,**kwargs):
        menu =Menu.get_menu_by_request_url(url=self.request.path_info)
        print(menu)
        if menu is not None:
            kwargs.update(menu)
        return super().get_context_data(**kwargs)