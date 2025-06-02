from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect, render

from .forms import CreateUserForm


def registerUser(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account was created for {username}")
            return redirect("login")

    else:
        form = CreateUserForm()

    context = {"form": form}

    return render(request, "registration/register.html", context)


def logoutUser(request):
    logout(request)
    return redirect("login")
