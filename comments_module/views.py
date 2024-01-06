from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from product_module.models import products
from .forms import comment_form
from .models import comment
# Create your views here.
class send_comment(View):
    def get(self,request):


        my_form=comment_form(request.GET)
        print(request.GET)
        if my_form.is_valid():

            my_product=products.objects.get(id=request.GET.get('pr'))
            new_comment=comment(product=my_product,subject=request.GET.get('subject'),comment_text=
                                request.GET.get('comment_text'),user_id=request.user.id)
            new_comment.save()

            return HttpResponse('')
        else:
            return HttpResponse('')


