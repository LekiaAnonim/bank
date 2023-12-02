from django.contrib import admin

# Register your models here.

# Register your models here.
from .models import Customer, Account, PostTransaction, Payment, CreateHistory, Currency, Bank, Card, CardType, Loan


class LoanAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone_number', 'amount')
    fields = ['email', 'phone_number', 'amount']

admin.site.register(Loan, LoanAdmin)
class BankAdmin(admin.ModelAdmin):
    list_display = ('bank_fullname', 'bank_abbr', 'bank_logo')
    fields = ['bank_fullname', 'bank_abbr', 'bank_logo']

admin.site.register(Bank, BankAdmin)

class CardAdmin(admin.ModelAdmin):
    list_display = ('account', 'card_number', 'expiry_date','card_type', 'cvv')
    fields = ['account', 'card_number', 'expiry_date', 'card_type', 'cvv']


admin.site.register(Card, CardAdmin)

class CardTypeAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'company_logo')
    fields = ['company_name', 'company_logo']


admin.site.register(CardType, CardTypeAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_on', 'middle_name', 'DOB', 'SSN',
                    'mobile_number', 'home_address', 'image')
    fields = [('user', 'middle_name', 'DOB'), ('SSN',
              'mobile_number', 'home_address', 'image')]


admin.site.register(Customer, CustomerAdmin)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('currency',)
    fields = ['currency',]


admin.site.register(Currency, CurrencyAdmin)


class CustomerInline(admin.TabularInline):
    model = CustomerAdmin


class AccountAdmin(admin.ModelAdmin):
    list_display = ('acct_id','created_on', 'customer', 'account_number', 'account_type',
                    'suspend_account', 'block_account', 'block_account_message', 'suspend_account_message', 'currency')
    fields = ['acct_id','customer', 'account_number',
              'account_type', 'suspend_account', 'block_account', 'block_account_message', 'suspend_account_message', 'currency']


admin.site.register(Account, AccountAdmin)


class AccountInline(admin.TabularInline):
    model = AccountAdmin


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('account', 'account_number', 'bank',
                    'account_name', 'amount', 'date', 'otp', 'receiver_email', 'routing_number', 'bank_address', 'remark')
    fields = ['account', 'account_number', 'bank',
              'account_name', 'amount', 'otp', 'receiver_email', 'routing_number', 'bank_address', 'remark']


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
