from django.urls import path
from .views import add_product,change_product_amount,delete_detail,load_order_page,load_step_2,load_step_3
urlpatterns=[path('add_product',add_product,name='addproduct')
             ,path('delete_product',delete_detail,name='deletedetail')
             ,path('change_amount',change_product_amount,name='changeamount')
             ,path('load_order_page',load_order_page.as_view(),name='load_order_page')
             ,path('load-step-2/<my_order>',load_step_2,name='load-step-2')
             ,path('load-step-3/<my_order>',load_step_3.as_view(),name='load-step-3')
             ]