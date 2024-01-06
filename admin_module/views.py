from django.contrib.auth.decorators import login_required
from django.core import serializers

from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, UpdateView, CreateView, DeleteView

import comments_module.models
from product_module.models import products
from .forms import Product_edit_form
from product_module.models import images,product_category,colors,brands
from order_module.models import order,order_detail
from user_Module.models import normal_user,user_messages
from .models import debts
def user_is_admin(func):
    def check_if_admin(*args,**kwargs):

        request=args[0]

        if request.user.is_authenticated and request.user.is_superuser:

            return func(*args,**kwargs)

        else:
            return redirect(reverse('login-user'))
    return check_if_admin

@method_decorator(user_is_admin,name='dispatch')
class admin_page_index(ListView):

    def get(self,request):
        return render(request,'admin_page_index.html')
class products_view_edit_delete(ListView):
    model = products
    template_name = 'admin_edit_delete_products.html'
    context_object_name = 'products'
    paginate_by = '4'
    ordering = ['-add_date']


class edit_product(UpdateView):
    model = products

    template_name = 'admin_edit_product.html'
    fields =list( {'title':0,'price':0,'short_description':0,'main_description':0,'category':0,'color':0,'brand':0,'is_active':0,'amount_left':0}.keys())
    def get_success_url(self,**kwargs):
        id=self.kwargs.get('pk')
        id_str=''
        ids=[]
        all_of_ids:str=self.request.POST.get('photos-to-delete')
        photo_to_add=self.request.FILES.get('photo-to-add')
        num=0
        for char in all_of_ids:
            if char !=',' and num!=len(all_of_ids)-1:
                id_str+=char

            else:
                if char==',':
                 ids.append(id_str)
                 id_str=''
                elif num==len(all_of_ids)-1:
                    id_str += char
                    ids.append(id_str)
            num+=1
        for img_id in ids:
            images.objects.get(id=img_id).delete()
        if photo_to_add is not None:
            new_img=images(picture=photo_to_add,product_id=id)
            new_img.save()



        url=reverse('load-edit-product',args=id)

        return url


class load_edit_product(View):
    def post(self,request:HttpRequest,id):
        pass
    def get(self,request,id):
        pr = products.objects.get(id=id)
        data={'title':pr.title,'price':pr.price,'short_description':pr.short_description
        ,'main_description':pr.main_description,'category':pr.category,'color':pr.color,'brand':pr.brand,'is_active':pr.is_active}
        new_form=Product_edit_form(data=data)


        return render(request,'admin_edit_product.html',context={'form':new_form,'product':pr})

# Create your views here.
def test(request):
    pr=request.GET.get('prid')
    pic=request._files.get('pic')
    new_img=images(product_id=pr)
    new_img.picture=pic

    return redirect(reverse('load_index_Page'))
class add_image(View):
    def post(self,request:HttpRequest,pid):
        img=request.POST.get('img')
        new_image=images(product_id=pid,picture=request._files.get('img'))
        new_image.save()
        print(request._files.get('img'))
        return redirect(reverse('load-edit-product',args=pid))
    def get(self,request:HttpRequest,prid):
        pass
class remove_image(View):
    def get(self,request):
        url=request.GET.get('url')
        imgs=images.objects.all()
        for obj in imgs:
            if obj.picture.url==url:
                obj.delete()
        return HttpResponse('')

class create_product(View):
    def post(self,request:HttpRequest):

        form=Product_edit_form(request.POST)
        if form.is_valid():
         obj=form.save()

         for img in list(request._files.getlist('img')):
             image=images(picture=img,product=obj)
             image.save()
         return  redirect(reverse('create-product'))
        else:
            return redirect(reverse('create-product'))


    def get(self,request):
        new_form = Product_edit_form()

        return render(request, 'admin_create_product.html', context={'fields': new_form})
class add_brand_color_category(View):
    def get(self,request,model):

        return render(request,'admin-add-category-color-brand.html',context={'model':model})
    def post(self,request,model):
        title=request.POST.get('title')
        print(request.POST)
        if model=='brand':
           brand= brands(title=title)
           brand.save()
        elif model=='color':
            color = colors(color=title)
            color.save()
        elif model=='category':
            cat = product_category(title=title)
            cat.save()
        return redirect(reverse('admin-index-page'))
class add_color_brand_category_ajax(View):
    def get(self,request):
        model=request.GET.get('model')
        title = request.GET.get('title')
        id=''
        print(title)
        if model == 'brand':
            brand = brands(title=title)
            brand.save()
            id=brand.id
        elif model == 'color':
            color = colors(color=title)
            color.save()
            id =color.id
        elif model == 'category':
            cat = product_category(title=title)
            cat.save()
            id = cat.id
        return JsonResponse({'id':id})
class remove_cat_brand_color(View):
    def get(self,request):
        type=request.GET.get('type')
        if type == 'brand':
           br=brands.objects.filter(id=request.GET.get('id'))
           br.delete()
        elif type == 'category':
            cat =product_category.objects.filter(id=request.GET.get('id'))
            cat.delete()
        elif type == 'color':
            clr = colors.objects.filter(id=request.GET.get('id'))
            clr.delete()
        return HttpResponse('')
class remove_prdocut(DeleteView):
    model=products
    success_url = reverse_lazy('admin-index-page')
    template_name = 'admin_page_index.html'
class view_orders(ListView):
    model = order
    template_name = 'orders.html'
    context_object_name = 'orders'
    ordering = ['order_date']

    def get_queryset(self):
        status=self.kwargs['status']
        print(status)
        query=super().get_queryset().filter(is_paid=True,status=status).all()
        print(query)
        return query
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        contex['status']=self.kwargs['status']
        return contex
class show_comments(ListView):
    model = comments_module.models.comment
    template_name = 'comments.html'
    context_object_name = 'comments'
    paginate_by = '4'
class confirm_reject_order(View):
    def get(self,request:HttpRequest,status):
     if status=='confirm':
         change_details=list(request.GET.get('change-details').split(','))
         delete_details=list(request.GET.get('delete-details').split(','))

         result=[]
         debt_value = request.GET.get('debtvalue')
         user_id = request.GET.get('userid')
         if ''  not in change_details or '' not in delete_details:
          if ''  not in change_details:
             for number in list(range(0, len(change_details), 2)):
                 index = number + 1
                 result.append([change_details[number], change_details[index]])
             details = order_detail.objects.filter(id__in=list([x[0] for x in result])).all()
             number = 0
             for y in details:
                 y.count = int(result[number][1])
                 y.save()
                 number += 1
          if '' not in delete_details:
             delete_details_list=order_detail.objects.filter(id__in=delete_details)
             for detail in delete_details_list:
                 detail.delete()
          new_debt = debts(user_id=user_id, amount=debt_value)
          new_debt.save()

         order_id = request.GET.get('orderid')
         order1=order.objects.filter(id=order_id).first()
         order1.status = 'confirmed'
         order1.save()
         message = request.GET.get('message')
         new_message=user_messages(reciever_user_id=user_id,message=message)
         new_message.save()
         print('confiremd')



     elif status=='reject':
         message=request.GET.get('message')
         user_id=request.GET.get('userid')
         order_number=request.GET.get('ordernumber')
         print('rejected')
         user_messages.objects.create(reciever_user_id=user_id,message=message).save()
         debts.objects.create(user_id=user_id,amount=request.GET.get('amount')).save()
         ord=order.objects.filter(order_number=order_number).first()

         ord.status='rejected'

         ord.save()
         print(ord.status)
     return HttpResponse('')
