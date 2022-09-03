from django.contrib import admin

# Register your models here.

# Register your models here.
from .models import Customer, Account, PostTransaction, Payment


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user','created_on', 'CUSTOMER_ID','middle_name', 'SSN',
                    'mobile_number', 'image')
    fields = [('user','CUSTOMER_ID', 'middle_name'), ('SSN',
              'mobile_number', 'image')]


admin.site.register(Customer, CustomerAdmin)
class CustomerInline(admin.TabularInline):
    model = CustomerAdmin


class AccountAdmin(admin.ModelAdmin):
    list_display = ('created_on', 'customer', 'account_number', 'account_type')
    fields = ['customer','account_number','account_type']


admin.site.register(Account, AccountAdmin)
class AccountInline(admin.TabularInline):
    model = AccountAdmin


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('account', 'account_number', 'bank',
                    'account_name', 'amount', 'date')
    fields = ['account', 'account_number', 'bank',
              'account_name', 'amount']


admin.site.register(Payment, PaymentAdmin)
class PaymentInline(admin.TabularInline):
    model = PaymentAdmin


class PostTransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'account_number', 'bank',
                    'account_name', 'amount', 'date')
    fields = ['account', 'account_number', 'bank',
              'account_name', 'amount']


admin.site.register(PostTransaction, PostTransactionAdmin)


class PostTransactionInline(admin.TabularInline):
    model = PostTransactionAdmin
