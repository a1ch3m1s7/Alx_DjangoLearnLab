from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, ProfileForm
from .models import Post

from datetime import datetime

def home(request):
    posts = Post.objects.all().order_by('-published_date')
    context = {
        'posts': posts,
        'year': datetime.now().year,
    }
    return render(request, 'blog/home.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Optionally set email lowercased
            user.email = form.cleaned_data['email'].lower()
            user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    return render(request, 'blog/register.html', {'form': form})

@login_required
def profile(request):
    # Edit user first/last/email via request.user (optional) + profile via ProfileForm
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        # allow editing of email/first/last via simple fields on template
        email = request.POST.get('email', request.user.email)
        first_name = request.POST.get('first_name', request.user.first_name)
        last_name = request.POST.get('last_name', request.user.last_name)

        if profile_form.is_valid():
            profile_form.save()
            # Update basic user fields
            user = request.user
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'profile_form': profile_form,
        'year': datetime.now().year,
    }
    return render(request, 'blog/profile.html', context)
