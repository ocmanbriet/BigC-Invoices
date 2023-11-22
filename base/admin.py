from django.contrib import admin
from .models import *

@admin.register(Orders)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id']
    search_fields = ['id', 'order_id']


@admin.register(CompanyName)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['order_id']
    search_fields = ['id', 'order_id']