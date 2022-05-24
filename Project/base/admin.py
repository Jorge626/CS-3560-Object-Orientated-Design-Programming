from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('customerID',)


class AccountAdmin(admin.ModelAdmin):
    readonly_fields = ('accountID', 'customerID')


class AddressAdmin(admin.ModelAdmin):
    readonly_fields = ('addressID', 'customerID')


class BillAdmin(admin.ModelAdmin):
    readonly_fields = ('billID', 'accountID')


class RateAdmin(admin.ModelAdmin):
    readonly_fields = ('tierID', )


# Register your models here.
admin.site.register(Bill, BillAdmin)
admin.site.register(Rate, RateAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Account, AccountAdmin)
