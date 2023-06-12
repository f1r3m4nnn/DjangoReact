from django.utils.html import format_html
from django.contrib import admin

from . import models



class OrderDetailInline(admin.TabularInline):
    model = models.OrderDetail
    extra = 0
    readonly_fields = ('commission',) # Tupla, não esquecer.

        

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderDetailInline]
    list_display = ('id', 'invoice_number', 'customer', 'seller', 'document_date', 'created', 'modified')
    readonly_fields = ('id', 'created', 'modified')



@admin.register(models.Item)
class ItemAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'created', 'modified', 'display_image', 'cod_prod')
    list_display = ('id', 'title', 'created', 'modified', 'stock', 'price')
    fieldsets = (
        (None, {'fields': (
                            'title', 'cod_prod', 'description', 'stock', 'price',
                            'display_image', 'image', 'commission_rate'
                )}),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('id', 'created', 'modified',),
        }),
    )


    def display_image(self, obj):
        return format_html(
                            '<a href="{}" target="_blank">'
                            '<div style="width:150px;height:150px;overflow:hidden;">'
                            '<img src="{}" style="object-fit:cover;width:150px;height:150px;" />'
                            '</div></a>', 
                            obj.image.url, obj.image.url
                            )
    

    display_image.short_description = 'Imagem'


    class Media:
        js = ('staticfiles/custom/custom.js',)



@admin.register(models.CommissionByDay)
class CommissionByDayAdmin(admin.ModelAdmin):
    list_display = ('id', 'day_of_week', 'min_commission', 'max_commission')
    readonly_fields = ('id',)



@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'created', 'modified')
    readonly_fields = ('id', 'created', 'modified')



@admin.register(models.Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'phone', 'email', 'created', 'modified')
    readonly_fields = ('id', 'created', 'modified', 'display_image')
    fieldsets = (
        (None, {'fields': ('name', 'phone', 'email', 'display_image', 'image',)}),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('created', 'modified',),
        }),
    )


    def display_image(self, obj):
        return format_html(
                            '<a href="{}" target="_blank">'
                            '<div class="boxgradient"  style="width:150px;height:150px;overflow:hidden;">'
                            '<img src="{}" style="object-fit:cover;width:150px;height:150px;  />'
                            '</div></a>', 
                            obj.image.url, obj.image.url
                            )


    display_image.short_description = 'Imagem'