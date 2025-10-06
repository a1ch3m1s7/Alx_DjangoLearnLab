# blog/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .models import Post
from .forms import PostForm
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

# Optional: existing home view can remain; we'll add class-based ListView for /posts/
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'  # new template
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 10  # optional

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'  # new template
    context_object_name = 'post'

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    # fields are taken from PostForm
    def form_valid(self, form):
        # Automatically set the author & published_date if needed
        form.instance.author = self.request.user
        # If you want to set published_date on create, use auto_now_add in model already
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        # Ensure the author isn't changed and remains the same
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# For template footer year context if you want consistent context
def site_year(request):
    return {'year': datetime.now().year}
