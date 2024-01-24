# restaurant_app/admin.py

from django.contrib import admin
from .models import Restaurant, Menu, MenuItem, Order, OrderItem

class MenuInline(admin.TabularInline):
    model = MenuItem
    extra = 1

class MenuAdmin(admin.ModelAdmin):
    inlines = [MenuInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]

admin.site.register(Restaurant)
admin.site.register(Menu, MenuAdmin)
admin.site.register(MenuItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
