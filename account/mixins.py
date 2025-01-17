from django.shortcuts import redirect


class RedirectAuthUser(object):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog-home')
        return super().dispatch(request, *args, **kwargs)
