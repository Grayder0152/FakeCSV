from django.views.generic.edit import FormView, View
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect

from .forms import LoginUserForm


class LoginFormViews(FormView):
    form_class = LoginUserForm
    success_url = "/"
    template_name = "user/login.html"

    def form_valid(self, form):
        self.user = form.get_user()
        self.user.save()
        login(self.request, self.user)
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
