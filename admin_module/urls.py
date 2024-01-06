from django.urls import path
from .views import admin_page_index,load_edit_product,test,add_image,remove_image,edit_product,create_product,add_brand_color_category,add_color_brand_category_ajax
from .views import remove_cat_brand_color,remove_prdocut,products_view_edit_delete,view_orders,show_comments,confirm_reject_order
urlpatterns=[path('admin-index-page',admin_page_index.as_view(),name='admin-index-page')
             ,path('load-edit-product/<id>',load_edit_product.as_view(),name='load-edit-product')
             ,path('test',test,name='test')
             ,path('add-image/<pid>',add_image.as_view(),name='add_image')
             ,path('delete_image',remove_image.as_view(),name='remove_image'),
              path('edit-product/<pk>',edit_product.as_view(),name='edit-product')
             ,path('create-product',create_product.as_view(),name='create-product')
             ,path('add-color-brand-category/<model>',add_brand_color_category.as_view(),name='add-color-brand-category')
             ,path('add-color-brand-category_ajax',add_color_brand_category_ajax.as_view(),name='add-color-brand-category_ajax')
,path('remove-color-brand-category_ajax',remove_cat_brand_color.as_view(),name='remove-color-brand-category_ajax'),
             path('remove_product/<pk>',remove_prdocut.as_view(),name='remove_prdouct')
             ,path('view_products',products_view_edit_delete.as_view(),name='view_products')
             ,path('view_orders/<status>',view_orders.as_view(),name='view_orders')
,path('show_comments',show_comments.as_view(),name='show_comments')
,path('confirm_reject_order/<status>',confirm_reject_order.as_view(),name='confirm_reject_order')
             ]
