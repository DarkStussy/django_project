from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

# auth
from main.forms import UserRegistrationForm, UserForm, ProfileUpdateImageForm, ProfileUpdatePNumberForm
from main.models import ProfileImage, Profile


def login_user(request):
    error = ''
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error = 'Login or password is incorrect'

    return render(request, 'main/login_user.html', {'error': error})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            profile_image = ProfileImage.objects.create(user=new_user)
            profile_image.save()
            profile_user = Profile.objects.create(user=new_user, phone_number='+')
            profile_user.save()
            return render(request, 'main/main.html')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'main/register.html', {'user_form': user_form})


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        pi_form = ProfileUpdateImageForm(request.POST, request.FILES, instance=request.user.profileimage)
        pn_form = ProfileUpdatePNumberForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and pn_form.is_valid():
            user_form.save()
            pn_form.save()
            messages.success(request, 'Your profile has been saved successfully!')
        elif pi_form.is_valid():
            pi_form.save()
            messages.success(request, 'Ваша аватарка успешно изменена!')
        else:
            messages.error(request, 'Unable to complete request')
        return redirect("profile")
    user_form = UserForm(instance=request.user)
    pass_form = PasswordChangeForm(user=request.user)
    pi_form = ProfileUpdateImageForm(instance=request.user.profileimage)
    pn_form = ProfileUpdatePNumberForm(instance=request.user.profile)
    return render(request=request, template_name="main/profile.html", context={"user": request.user,
                                                                               "user_form": user_form,
                                                                               "pass_form": pass_form,
                                                                               "pi_form": pi_form,
                                                                               "pn_form": pn_form})


def main(request):
    return render(request, 'main/main.html')


@login_required
def home(request):
    return render(request, 'main/home.html')
