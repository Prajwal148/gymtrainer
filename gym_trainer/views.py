from django.shortcuts import redirect
from django.views.generic import TemplateView
from userprofile.models import UserProfile

class HomeView(TemplateView):
    template_name = 'index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('test')
        return super().dispatch(request, *args, **kwargs)


class TestPage(TemplateView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        try:
            context['profile'] = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            context['profile'] = None
        return context


class ThanksPage(TemplateView):
    template_name = 'thanks.html'
