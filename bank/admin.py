from django.contrib import admin

# Register your models here.

# Register your models here.
from .models import Customer, Account, PostTransaction, Payment


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user','created_on', 'middle_name','DOB', 'SSN',
                    'mobile_number', 'home_address', 'image')
    fields = [('user', 'middle_name', 'DOB'), ('SSN',
              'mobile_number', 'home_address', 'image')]


admin.site.register(Customer, CustomerAdmin)
class CustomerInline(admin.TabularInline):
    model = CustomerAdmin


class AccountAdmin(admin.ModelAdmin):
    list_display = ('created_on', 'customer', 'account_number', 'account_type', 'suspend_account', 'block_account')
    fields = ['customer', 'account_number',
              'account_type', 'suspend_account', 'block_account']


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
    list_display = ('account', 'bank', 'amount', 'date')
    fields = ['account', 'bank', 'amount']


admin.site.register(PostTransaction, PostTransactionAdmin)


class PostTransactionInline(admin.TabularInline):
    model = PostTransactionAdmin
