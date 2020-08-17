import six
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from .forms import NewUserCreationForm, LoginForm, AvatarChangeForm, CoverChangeForm
from .models import User

from blog.forms import NewPostForm
from blog.models import Blog, Comment
from gallary.forms import BlogImageNewForm


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active)
        )


account_activation_token = TokenGenerator()


def index(request):
    context = {}

    if request.GET.get('token'):
        user = get_object_or_404(User, pk=request.GET['token'])
        context.update({
            'login_form': LoginForm(initial={'email': user.email})
        })

    if request.user.is_authenticated:
        context.update({
            'blogs': Blog.objects.all(),
            'recent_blogs': Comment.objects.all().order_by('-create_at')[:6],
            'blog_form': NewPostForm(),
            'image_form': BlogImageNewForm(),
        })
        return render(request, 'user/index.html', context)
    else:
        context.update({
            'register_form': NewUserCreationForm(),
            'login_form': LoginForm(),
        })
        return render(request, 'guest/index.html', context)


@login_required
def profile(request, pk):
    context = {
        'user': get_object_or_404(User, id=pk),
        'avatar_form': AvatarChangeForm(),
        'cover_form': CoverChangeForm(),
    }
    return render(request, 'user/profile.html', context)


def LOGIN(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request.POST)
            if form.is_valid():
                user = authenticate(
                    email=form.cleaned_data.get('email'),
                    password=form.cleaned_data.get('password')
                )
                if user:
                    login(request, user)
                    return redirect('user:profile_page', pk=user.id)
            else:
                for error in form.errors['__all__']:
                    messages.error(request, error)
            context = {
                'login_form': form
            }
        else:
            context = {
                'login_form': LoginForm()
            }
        return render(request, 'user/login.html', context)
    else:
        messages.warning(request, 'You are already logged in!')
        return redirect('user:home_page')


def REGISTER(request):
    if request.method == 'POST':
        form = NewUserCreationForm(request.POST)
        if form.is_valid():
            user_form = form.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('settings/active_email.html', {
                'user': user_form,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user_form.pk)),
                'token': account_activation_token.make_token(user_form),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'Please, Check Your Email we\'ve sent an activation link for you Profile.')
        else:
            messages.error(request, 'Please make sure all the inputs are right!')
        context = {
            'register_form': form
        }
    else:
        context = {
            'register_form': NewUserCreationForm()
        }
    return render(request, 'user/register.html', context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        User(request, user)
        messages.success(request, 'Profile Activated')
        return redirect(f'{reverse("user:home_page")}?token={user.pk}')
    else:
        return HttpResponse('Activation link is invalid!')


def LOGOUT(request):
    logout(request)
    return redirect('user:home_page')


def avatar_change(request):
    if request.method == 'POST':
        form = AvatarChangeForm(request.POST, request.FILES)
        if form.is_valid():
            user = get_object_or_404(User, pk=request.user.id)
            user.profile_pic = request.FILES['profile_pic']
            user.save()
            messages.success(request, 'Image Profile Changed')
        else:
            messages.success(request, 'Error while changing image profile')
    return redirect('user:profile_page', pk=request.user.id)


def cover_change(request):
    if request.method == 'POST':
        form = CoverChangeForm(request.POST, request.FILES)
        if form.is_valid():
            user = get_object_or_404(User, pk=request.user.id)
            user.cover_pic = request.FILES['cover_pic']
            user.save()
            messages.success(request, 'Image Profile Changed')
        else:
            messages.success(request, 'Error while changing image profile')
    return redirect('user:profile_page', pk=request.user.id)
