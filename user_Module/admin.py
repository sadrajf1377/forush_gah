from django.contrib import admin
from .models import normal_user,user_messages
# Register your models here.
admin.site.register(normal_user)
class user_messages_settings(admin.ModelAdmin):
    readonly_fields = ['creation_date']

admin.site.register(user_messages,user_messages_settings)