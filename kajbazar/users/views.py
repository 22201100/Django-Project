from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, PasswordChangeView, LogoutView
from django.urls import reverse_lazy
from .forms import UserRegisterForm, UserLoginForm, UserUpdateForm, ProfileUpdateForm, CustomPasswordChangeForm
from courses.models import Course, Enrollment

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('home')

@login_required
def dashboard(request):
    # Get courses created by the user
    created_courses = Course.objects.filter(created_by=request.user)
    
    # Get courses the user is enrolled in
    enrolled_courses = Course.objects.filter(enrollments__user=request.user)
    
    # Mock activity data (in a real app, you'd have an Activity model)
    activities = [
        {
            'date': '2023-05-15',
            'action': 'Enrolled in',
            'course': 'Web Development Basics',
            'status': 'Completed',
            'status_class': 'bg-green-100 text-green-800'
        },
        {
            'date': '2023-05-10',
            'action': 'Created course',
            'course': 'Introduction to Python',
            'status': 'Active',
            'status_class': 'bg-blue-100 text-blue-800'
        },
        {
            'date': '2023-05-05',
            'action': 'Enrolled in',
            'course': 'Digital Marketing',
            'status': 'In Progress',
            'status_class': 'bg-yellow-100 text-yellow-800'
        }
    ]
    
    context = {
        'created_courses': created_courses,
        'enrolled_courses': enrolled_courses,
        'activities': activities
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('profile')
    
    def form_valid(self, form):
        messages.success(self.request, 'Your password has been updated!')
        return super().form_valid(form)

class CustomLogoutView(LogoutView):
    next_page = '/'
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
