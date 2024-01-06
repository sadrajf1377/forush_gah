from django.contrib import admin
from .models import order,order_detail
# Register your models here.
admin.site.register(order)
admin.site.register(order_detail)