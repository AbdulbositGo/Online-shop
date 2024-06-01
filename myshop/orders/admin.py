import csv
import datetime
from django.urls import reverse
from django.contrib import admin
from django.http import HttpResponse
from django.utils.safestring import mark_safe

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return ''
order_payment.short_description = 'Stripe payment'


def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    content_description = f'attachment; filename={opts.verbose_name_plural } { time }.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_description
    writer = csv.writer(response)
    fields = [field for field in opts.get_fields()\
              if not field.many_to_many and not field.one_to_many]
    writer.writerow([(field.verbose_name).title() for field in fields])
    data_rows = []
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        data_rows.append(data_row)
    writer.writerows(data_rows)
    return response

export_to_csv.short_description = "Export to csv"

def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'paid', order_detail, 'first_name', 'last_name',
                    'email','address', 'postal_code', 'city', 
                    order_payment, 'created','updated', ]
    list_filter = ['paid', 'created', 'updated']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
