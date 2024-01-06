from django.http import HttpResponse, JsonResponse, HttpRequest
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from product_module.models import products
from .models import order,order_detail,reciver_info
# Create your views here.
def add_product(request):
    count=int(request.GET.get('count'))

    user_Id=request.user.id
    product_id=request.GET.get('prid')
    if count>products.objects.get(id=product_id).amount_left:

        return JsonResponse(data={'status':'failed'})
        return
    new_order,bl=order.objects.get_or_create(is_paid=False,user_id=user_Id)
    new_order.save()
    pr=products.objects.filter(id=product_id).first()
    pr.amount_left-=count
    pr.save()
    detail_exists = order_detail.objects.filter(parent_order=new_order, product_id=product_id).exists()
    new_detail, bb = order_detail.objects.get_or_create(parent_order=new_order, product_id=product_id)

    new_detail.count=count if not detail_exists else count+new_detail.count

    new_detail.save()

    return JsonResponse(data={'total_price':'{:,}'.format(new_order.get_total_price()),'pricevl':'{:,}'.format(new_detail.total_price),'countvl':new_detail.count
                              ,'detailid':new_detail.id,'status':'succeed'}
                        )
def change_product_amount(request):

    amount =int(request.GET.get('amount'))

    user_id = request.user.id
    product_id =int(request.GET.get('prid'))
    pr = products.objects.filter(id=product_id).first()
    pr.amount_left -= amount
    pr.save()
    new_order = order.objects.filter(is_paid=False, user_id=user_id).first()
    new_detail = order_detail.objects.filter(parent_order=new_order, product_id=product_id).first()
    new_detail.count=amount
    new_order.check_if_empty()
    new_detail.save()
    return JsonResponse(data={'detailprice':'{:,}'.format(new_detail.total_price),'totalprice':
        '{:,}'.format(new_order.get_total_price())})

def delete_detail(request):
    if request.method=='GET':
     user_id = request.user.id
     detail_id = request.GET.get('dtid')

     new_order = order.objects.filter(is_paid=False, user_id=user_id).first()
     new_detail = order_detail.objects.filter(parent_order=new_order, id=detail_id).first()
     pr = products.objects.filter(id=new_detail.product_id).first()
     pr.amount_left +=new_detail.count
     pr.save()
     new_detail.delete()


     return JsonResponse(data={'totalprice':'{:,}'.format(new_order.get_total_price())})

class load_order_page(ListView):
    template_name = 'step-1.html'
    model = order_detail
    context_object_name = 'details'
    def get_queryset(self):

        query=super().get_queryset().filter(parent_order__is_paid=False,parent_order__user=self.request.user)

        return query
    def get_context_data(self, *, object_list=None, **kwargs):
        contex=super().get_context_data()
        contex['order']= order.objects.filter(is_paid=False,user_id=self.request.user.id).first()
        return contex

def load_step_2(request,my_order:order):
    return render(request,'step-2.html',{'order':my_order})
class load_step_3(View):
    def post(self,request:HttpRequest,my_order):
        information={'first_name':request.POST.get('first_name'),'last_name':request.POST.get('last_name'),'phone':request.POST.get('telephone')
                     ,'email':request.POST.get('email'),'address':request.POST.get('address'),'city':request.POST.get('city'),
                     'postal_code':request.POST.get('postal_code')}

        new_info,bb=reciver_info.objects.get_or_create(id=order.objects.filter(user__username=my_order).first().id)
        new_info.update_fields(information)
        new_info.save()
        #custom_order=order.objects.filter(user__username=my_order).first()
        #custom_order.recive_info.save(update_fields=information)
        #custom_order.save()
        return render(request,'step-3.html')