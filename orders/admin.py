from django.contrib import admin

from orders.models import Order, OrderItem

class OrderItemTabularAdmin(admin.TabularInline):
    model = OrderItem
    fields = ('product', 'name', 'price', 'quantity')



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'users',
        'requires_delivery',
        'status',
        'payment_on_get',
        'is_paid',
        'created_timestamp',
    )

    search_fields = (
        '=id',
        'users__username',
        'phone_number',
        'status',
    )
    readonly_fields = ('created_timestamp',)
    list_filter = (
        'requires_delivery',
        'status',
        'payment_on_get',
        'is_paid',
        'created_timestamp',
    )
    inlines = (OrderItemTabularAdmin,)
