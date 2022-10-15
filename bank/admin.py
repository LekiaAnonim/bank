from django.contrib import admin

# Register your models here.

# Register your models here.
from .models import Customer, Account, PostTransaction, Payment, CreateHistory


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_on', 'middle_name', 'DOB', 'SSN',
                    'mobile_number', 'home_address', 'image')
    fields = [('user', 'middle_name', 'DOB'), ('SSN',
              'mobile_number', 'home_address', 'image')]


admin.site.register(Customer, CustomerAdmin)


class CustomerInline(admin.TabularInline):
    model = CustomerAdmin


class AccountAdmin(admin.ModelAdmin):
    list_display = ('created_on', 'customer', 'account_number', 'account_type',
                    'suspend_account', 'block_account', 'block_account_message', 'suspend_account_message')
    fields = ['customer', 'account_number',
              'account_type', 'suspend_account', 'block_account', 'block_account_message', 'suspend_account_message']


admin.site.register(Account, AccountAdmin)


class AccountInline(admin.TabularInline):
    model = AccountAdmin


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('account', 'account_number', 'bank',
                    'account_name', 'amount', 'date', 'otp', 'receiver_email', 'routing_number', 'bank_address')
    fields = ['account', 'account_number', 'bank',
              'account_name', 'amount', 'otp', 'receiver_email', 'routing_number', 'bank_address']


admin.site.register(Payment, PaymentAdmin)


class PaymentInline(admin.TabularInline):
    model = PaymentAdmin


class PostTransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'company_name', 'amount', 'date')
    fields = ['account', 'company_name', 'amount']


admin.site.register(PostTransaction, PostTransactionAdmin)


class PostTransactionInline(admin.TabularInline):
    model = PostTransactionAdmin


class CreateHistoryAdmin(admin.ModelAdmin):
    list_display = ('account', 'company_name', 'amount', 'date', 'top_up_type')
    fields = ['account', 'company_name', 'amount', 'date', 'top_up_type']


admin.site.register(CreateHistory, CreateHistoryAdmin)


class CreateHistoryInline(admin.TabularInline):
    model = CreateHistoryAdmin
