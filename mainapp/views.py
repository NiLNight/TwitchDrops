from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from django.views.generic import TemplateView
from .forms import UserRegistrationForm, UserLoginForm


class MainView(TemplateView):
    template_name = 'main.html'


class UserRegistrationView(CreateView):
    template_name = 'registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('main')  # Замените 'main' на имя вашего URL

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            auth_login(self.request, user)
            return HttpResponseRedirect(self.success_url)


class UserLoginView(FormView):
    template_name = 'login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('main')  # Перенаправление на главную страницу после входа

    def form_valid(self, form):
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)