from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.urls import reverse

from NBA.models import HiddenGamePreferences
from .forms import CustomUserCreationForm

def dashboard(request):
    '''
    Displays a dashboard for either the currently logged in user or a guest.
    This dashboard contains links for loggin in, logging out, and changing
    a password.
    Params:
        request: Instance representing the HTTP request that queried this view.
    Returns:
        HTTP response representing the user dashboard.
    '''
    if request.user.is_authenticated:
        scores_hidden = HiddenGamePreferences.objects.get(user=request.user).hide_scores
    else:
        scores_hidden = False
    context = {
        'scores_hidden': scores_hidden,
    }
    return render(request, 'users/dashboard.html', context)


def register(request):
    '''
    Displays a form used to create a new custom user. This custom user contains the
    normal fields associated with a Django User, along with their first name.
    Params:
        request: Instance representing the HTTP request that queried this view.
    Returns:
        HTTP response representing the new user registration form if the form has
        not been submitted, otherwise a redirected HTTP response to the user dashboard.
    '''
    # Form has not been submitted
    if request.method == "GET":
        # Display form
        return render(request, "users/register.html", {'form': CustomUserCreationForm})
    # Form has been submitted
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        # Form has been submitted & is valid
        if form.is_valid():
            user = form.save()
            HiddenGamePreferences.objects.create(user=user)
            login(request, user)
            return redirect(reverse("users:dashboard"))
        # Form has been submitted but is invalid
        else:
            return render(request, "users/register.html", {'form': CustomUserCreationForm})