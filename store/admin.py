from django.contrib import admin
from .models import Item, OrderItems, Order, Category, BillingAddress, Coupon

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered', 'being_delivered', 'received', 'refund_requested', 'refund_granted','billing_address', 'coupon']
    list_display_links = ['user','billing_address', 'coupon']
    search_fields = ['user__username', 'ordered', 'being_delivered', 'received', 'refund_requested', 'refund_granted', 'ref_code']
    list_filter = ['user', 'ordered', 'being_delivered', 'received', 'refund_requested', 'refund_granted']
    
admin.site.register(Order, OrderAdmin)


admin.site.register(OrderItems)
admin.site.register(BillingAddress)
admin.site.register(Coupon)

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)} 

admin.site.register(Item, ItemAdmin)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)


    
