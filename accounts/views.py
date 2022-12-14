from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from accounts.forms import LoginForm, RegistrationForm, ChangePasswordForm
from django.contrib.auth.decorators import login_required
from accounts.forms import UserEditForm, ProfileEditForm
from accounts.models import Profile



@login_required
def edit(request):

    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, 
                                        data=request.POST,
                                        files=request.FILES)
    
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect ("tasks:list")
    
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request,
                "accounts/edit.html",
                {"user_form": user_form, "profile_form": profile_form},)



def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, "accounts/registration_complete.html",{"new_user": new_user})
    else:
        form = RegistrationForm()
    
    return render(request, "accounts/register.html", {"user_form": form})


           
class LoginView(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request,
                username = cd["username"],
                password = cd["password"]
            )
            if user is None:
                return HttpResponse("???????????????????????? ?????????? ??/?????? ????????????")
            if not user.is_active:
                return HttpResponse("?????? ?????????????? ????????????????????????")
            
            login(request,user)
            return HttpResponse("?????????? ??????????????????")
        
        return render(request,"accounts/login.html",{"form": form})
    
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'accounts/login.html', {'form': form})
    
