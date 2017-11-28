from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views.generic import FormView


class RegistrationView(FormView):
    form_class = UserCreationForm
    success_url = None
    template_name = 'registration.html'

    def form_valid(self, form: UserCreationForm) -> HttpResponse:
        user = form.save()
        auth_login(self.request, user)
        return HttpResponseRedirect(reverse('index'))
