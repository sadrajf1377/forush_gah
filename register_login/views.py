from django.contrib.auth import login, logout
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View

import polls.templatetags.polls_extra
from .forms import register_form
from user_Module.models import normal_user
from utils.email_services import send_email
# Create your views here.
class register_user(View):
    def post(self,request:HttpRequest):
        rg_form=register_form(request.POST)
        if rg_form.is_valid():
            passwords_matches:bool=rg_form.cleaned_data.get('password')==rg_form.cleaned_data.get('password_repeat')
            email_exists:bool=normal_user.objects.filter(email__iexact=rg_form.cleaned_data.get('email')).first()
            activate_code = get_random_string(72)
            email_valid= send_email(template_name='activate_acount.html',to=rg_form.cleaned_data.get('email'),subject='فعال سازی اکانت',contex={'code':activate_code}) ==1
            print(email_valid)
            if passwords_matches and not email_exists and email_valid:

                new_user:normal_user=normal_user(email=rg_form.cleaned_data.get('email'),activation_code=activate_code
                                                 ,username=rg_form.cleaned_data.get('email'),is_active=False)

                new_user.set_password(rg_form.cleaned_data.get('password'))
                new_user.save()
                return render(request,'register_done.html')
            else:
                rg_form.add_error('password_repeat','تکرار پسوورد اشتباه است' if not passwords_matches else '')
                rg_form.add_error('email', 'این ایمیل قبلا ثبت شده است' if email_exists else '')
                rg_form.add_error('email', 'ایمیل وارد شده معتبر نمی باشد' if not email_valid else '')
                return render(request, 'register_page.html', {'register_form':rg_form})

    def get(self,request:HttpRequest):
        contex={'register_form':register_form(None)}

        return render(request, 'register_page.html', contex)

def activate_user(request,activate_code):
    user_custom=normal_user.objects.all().get(activation_code=activate_code)
    user_custom.is_active=True
    user_custom.save()
    print(user_custom.get_full_name())
    return HttpResponse("اکانت شما با موفقیت فعال شد")


class login_user(View):
    def post(self,request:HttpRequest):

        try:
            email_check = normal_user.objects.all().filter(email__iexact=request.POST.get('email')).first()
            user_found=email_check.check_password(request.POST.get('password'))
        except:
            user_found=False
        if user_found:
            login(request,email_check)
            polls.templatetags.polls_extra.current_user=request.user

            return redirect(reverse('load_index_Page'))
        else:
            contex={'error':'ایمیل یا کلمه عبور اشتباه است!'}
            return render(request,'login_page.html',contex)
    def get(self,request:HttpRequest):
        return render(request,'login_page.html')

def logout_user(request):
    logout(request)
    polls.templatetags.polls_extra.current_user = None
    return redirect(reverse('load_index_Page'))