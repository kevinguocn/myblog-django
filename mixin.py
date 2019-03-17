from django.contrib.auth.decorators import login_required


class AdminLoginRequiredMixin(object):
    @classmethod
    def as_view(cls,**init_kwargs):
        view = super(AdminLoginRequiredMixin, cls).as_view(*init_kwargs)
        return login_required(view)