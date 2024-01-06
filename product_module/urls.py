from django.urls import path
from .views import index_page,product_dtails,shop_page,set_filters,add_user_to_wish_list
urlpatterns=[
    path('',index_page.as_view(),name='load_index_Page')
             ,path('show-product-details/<pk>',product_dtails.as_view(),name='show-product-details')
             ,path('shop_page',shop_page.as_view(),name='shop_page'),
             path('set_filters',set_filters.as_view(),name='set_filters')
    ,path('add_user_to_wishlist',add_user_to_wish_list.as_view(),name='add_user_to_wishlist')

             ]