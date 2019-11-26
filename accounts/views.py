from django.contrib.auth import authenticate, login

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView

from accounts.forms import CustomUserSignUpForm


class RegistrationView(CreateView):
    template_name = 'accounts/registration.html'
    form_class = CustomUserSignUpForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        to_return = super().form_valid(form)
        user = authenticate(
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password1"],
        )
        login(self.request, user)
        return to_return
