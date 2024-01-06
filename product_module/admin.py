from django.contrib import admin
from django.http import HttpRequest

from .models import products,images,colors,product_category,brands,product_wish_list
# Register your models here.
class product_settings(admin.ModelAdmin):
    list_display = ['__str__','price','is_active','url']

class image_settings(admin.ModelAdmin):

    list_display = ['__str__','picture']
    def delete_queryset(self, request, queryset:images):
         for obj in queryset:
             obj.picture.delete()
             obj.delete()
admin.site.register(products,product_settings)
admin.site.register(images,image_settings)
admin.site.register(colors)
admin.site.register(product_category)
admin.site.register(brands)
admin.site.register(product_wish_list)