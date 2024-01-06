from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

import polls.templatetags.polls_extra
from .models import products,product_category,brands,product_wish_list
from comments_module.forms import comment_form
from user_Module.models import normal_user,user_messages
# Create your views here.
conditions={'brs':[x.id for x in brands.objects.all() if brands.objects.exists()]
    ,'cats':[x.id for x in product_category.objects.all() if product_category.objects.exists()],'min_price':0,
            'max_price':products.objects.order_by('price').last().price if products.objects.count()>0 else 0}
use_query=False
class index_page(ListView):
    template_name = 'index_page.html'
    model = products
    context_object_name = 'products'
    def get_queryset(self):
        query=super().get_queryset()
        query.filter(is_active=True).all()

        if self.request.user.is_authenticated:
         polls.templatetags.polls_extra.current_user=self.request.user
        print(self.request.session.values())
        return query
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        contex['latest_products']=products.objects.order_by('add_date')[:3]

        return contex

class product_dtails(DetailView):
    model = products
    template_name = 'product_details.html'
    context_object_name = 'product'
    def get_context_data(self,**kwargs):

        contex=super().get_context_data()
        contex['comments_form']=comment_form()

        return contex

class shop_page(ListView):
    model = products
    context_object_name = 'products'
    template_name = 'shop_page.html'
    paginate_by = 6
    def get_queryset(self):
        global use_query
        if use_query:
         query = super().get_queryset().filter(category__id__in=conditions['cats'], brand__id__in=conditions['brs'],price__lte=conditions['max_price']
                                               ,price__gte=conditions['min_price'])

         use_query = False
        else:
            query=super().get_queryset()

        return query
    def get_context_data(self, *, object_list=None, **kwargs):

        contex=super().get_context_data()
        contex['brands']=brands.objects.all()
        contex['categories']=product_category.objects.all()
        orderd_by_price=products.objects.order_by('price')
        contex['min_price']=orderd_by_price.first().price
        contex['max_price']=orderd_by_price.last().price
        return contex

class set_filters(View):
    def get(self,request:HttpRequest):
        print(request.GET.get('brs'))
        if len(request.GET.get('brs')) != 0:
         brs=[int(x) for x in list(request.GET.get('brs')) if x!=',']

         conditions['brs'] = brs
        if len(request.GET.get('cats'))!=0:
         cats=[int(x) for x in list(request.GET.get('cats')) if x!=',']
         conditions['cats'] = cats
        if request.GET.get('minprice')!='' and request.GET.get('maxprice')!='':
         min_price=request.GET.get('minprice')
         max_price=request.GET.get('maxprice')

         min_price=(min_price.replace('$',''))
         max_price =(max_price.replace('$', ''))

         conditions['min_price'] = int(min_price)
         conditions['max_price'] = int(max_price)

        global use_query
        use_query=True




        return HttpResponse('')

@method_decorator(login_required,name='dispatch')
class add_user_to_wish_list(View):
    def get(self,request):

        user_id=request.GET.get('user-id')
        product_title=request.GET.get('product-title')
        user=normal_user.objects.get(id=user_id)
        product=products.objects.get(title__iexact=product_title)
        wish_list,bb=product_wish_list.objects.get_or_create(product_id=product.id)
        message=''
        update_status=''
        if wish_list.users.filter(id=user_id).exists():
            wish_list.users.remove(user)
            wish_list.save()
            message=f'کالای  {product_title}از لیست علاقه مندی های شما حذف شد '
            update_status='remove'
        else:
         wish_list.users.add(user)
         wish_list.save()
         message=f'کالای {product_title}به لیست علاقه مندی های شما اضافه شد '
         update_status = 'add'

        return JsonResponse(data={'message':message,'st':update_status})
