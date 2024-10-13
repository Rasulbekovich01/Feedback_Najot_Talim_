from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import FormView

from config.settings import EMAIL_DEFAULT_SENDER
from user.authentication_form import AuthenticationForm
from user.forms import RegisterModelForm, EmailSendForm
from user.models import User
from user.token import account_activation_token


# Create your views here.


class LoginPageView(LoginView):
    redirect_authenticated = True
    form_class = AuthenticationForm
    template_name = 'user/login.html'
    success_url = reverse_lazy('success')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid Email or Password')
        return self.render_to_response(self.get_context_data(form=form))


def register_page(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('user/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            send_mail(
                'Welcome to Najot ta\'lim',
                message,
                EMAIL_DEFAULT_SENDER,
                [user.email],
                fail_silently=False,
            )
            return HttpResponse('<h1>Please confirm your email address to complete the registration</h1>')
    else:
        form = RegisterModelForm()
    context = {'form': form}
    return render(request, 'user/register.html', context)


class SendEmailView(FormView):
    template_name = 'user/sending_mail.html'
    form_class = EmailSendForm
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


def logout_page(request):
    # if request.method == 'POST':
    logout(request)
    return redirect('success')


def success(request):
    return render(request, 'user/success.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return HttpResponse('<h1>Thank you for your email confirmation. Now you can login your account.</h1>')
    else:
        return HttpResponse('<h1>Activation link is invalid!</h1>')
