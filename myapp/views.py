from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import login
from .forms import StudentSignUpForm
from django.contrib.auth import logout
from .models import Resource, Mark, Announcement, Query
import datetime
from django.contrib import messages


def my_login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('/admin/')
        else:
            return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/admin/')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')


def home_view(request):
    resources = Resource.objects.all()
    marks = Mark.objects.filter(student=request.user)
    announcements = (Announcement.objects.filter(for_all=True) | Announcement.objects.filter(
        specific_student=request.user)).order_by('-created_at')
    context = {
        'user': request.user,
        'welcome_message': "Distributed Systems Dashboard",
        'resources': resources,
        'marks': marks,
        'announcements': announcements,
    }
    return render(request, 'home.html', context)


def register(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
    else:
        form = StudentSignUpForm()
    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def submit_query(request):
    if request.method == "POST":
        message = request.POST.get('message', '')
        query = Query(student=request.user, message=message)
        query.save()
        messages.success(request, 'Submitted query successfully')
        return redirect('/home')
    return redirect('/home')
