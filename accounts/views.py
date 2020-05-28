from django.shortcuts import render,redirect
from .forms import *
from .models import *
from django.contrib import messages

def profile(request):
    if request.method == 'POST':
        u_form = UserForm(request.POST, instance=request.user)
        p_form = ProfileForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile')

    else:
        u_form = CreateUserForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'accounts/userprofile.html', context)


from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.views import View

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

from .tokens import activation_token

from django.contrib.auth.models import User
from django.core.mail import send_mail

from django.contrib import messages


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = CreateUserForm()
        template_name = "accounts/register.html"
        return render(request, template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            subject = "Activate your account"
            domain_url = get_current_site(request)
            message = render_to_string(
                "accounts/activation_message.html",
                {
                    "domain": domain_url.domain,
                    "user": user,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get('email')
            send_mail(subject, message, 'Email@gmail.com', [to_email])
            activation_msg = "Open your email to activate account."
            return render(
                request, "accounts/activate_email.html", {"activation_msg": activation_msg}
            )
        
        template_name = 'accounts/register.html'
        return render(request, template_name, {"form": form})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        return redirect('login')
    else:
        return render(request, "accounts/activation_fail.html")


def loginuser(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username and Password Does not Match')

        context = {}
        return render(request, 'accounts/login.html', context)
    
def logoutuser(request):
	logout(request)
	return redirect('login')


def dashboard(request):
    return render(request, "accounts/dashboard.html", {})
    
