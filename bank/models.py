from django.db import models
from localflavor.us.models import USSocialSecurityNumberField
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.template import Context, Template
from cloudinary.models import CloudinaryField
from django.core.validators import MaxValueValidator, RegexValidator


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    DOB = models.DateField(null=True, blank=True)
    SSN = USSocialSecurityNumberField(max_length=9)
    mobile_number = PhoneNumberField()
    home_address = models.CharField(max_length=255, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    image = CloudinaryField('image')

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} \n {self.user.email}'

    def account_name(self):
        return f'{self.user.first_name} {self.middle_name} {self.user.last_name}'

    def get_absolute_url(self):
        return reverse('bank:customer-update', kwargs={'pk': self.pk})

    account_name.short_description = 'Customer'


class Account(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, null=True)
    CHOICES = (
        ('Checking', 'Checking'),
        ('Savings', 'Savings'),
        ('Time Deposit', 'Time Deposit'),
        ('Personal Loan', 'Personal Loan'),
        ('Credit Line', 'Credit Line'),
        ('DH Real Estate Loan', 'DH Real Estate Loan'),
        ('Business Loan', 'Business Loan'),
        ('Real Estate Loan', 'Real Estate Loan'),

    )
    account_type = models.CharField(max_length=300, choices=CHOICES, null=True)
    account_number = models.CharField(max_length=12, unique=True, null=True, validators=[
                                      RegexValidator(r'^\d{1,12}$')])
    created_on = models.DateField(auto_now_add=True)
    suspend_account = models.BooleanField(default=False)
    block_account = models.BooleanField(default=False)
    block_account_message = models.TextField(
        default='This account has been blocked Kindly contact the administrator to learn more. Or, enter a valid username and password.')
    suspend_account_message = models.TextField(
        default='This account has been suspended Kindly contact the administrator to learn more. Or, enter a valid username and password.')
    
    CURRENCY_CHOICES = (
        ('$', 'Dollar'),
        ('£', 'Pounds' ),
        ('€', 'Euro'),
        ('₩', 'Korean Won'),
        ('₹', 'Indian Rupees'),
        ('¥', 'Chinese Yuan'),
    )
    currency = models.CharField(max_length=100, choices=CURRENCY_CHOICES, default='Dollar', null=True)

    class Meta:
        ordering = ['account_type', 'created_on']

    def __str__(self):
        return f'{self.customer}'

    def account_name(self):
        return f'{self.customer.user.first_name} {self.customer.middle_name} {self.customer.user.last_name}'

    def get_absolute_url(self):
        return reverse('bank:account-update', kwargs={'pk': self.pk})


class PostTransaction(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True)
    company_name = models.CharField(max_length=255, null=True)
    date = models.DateField(null=True)
    amount = models.IntegerField(blank=False, null=False)

    def get_absolute_url(self):
        return reverse('bank:posttransaction-update', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date']


class CreateHistory(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True)
    company_name = models.CharField(max_length=255, null=True, blank=True)
    date = models.DateField()
    amount = models.IntegerField(blank=False, null=False)
    CHOICES = (
        ('Credit', 'Credit'),
        ('Debit', 'Debit'),
    )

    top_up_type = models.CharField(max_length=300, choices=CHOICES, null=True)

    def get_absolute_url(self):
        return reverse('bank:createhistory-update', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date']

class Currency(models.Model):
    CURRENCY_CHOICES = (
        ('$', 'Dollar'),
        ('£', 'Pounds' ),
        ('€', 'Euro'),
        ('₩', 'Korean Won'),
        ('₹', 'Indian Rupees'),
        ('¥', 'Chinese Yuan'),
    )
    currency = models.CharField(max_length=100, choices=CURRENCY_CHOICES, default='$', null=True)

    class Meta:
        verbose_name_plural = "currencies"

    def get_absolute_url(self):
        return reverse('bank:currency-update', kwargs={'pk': self.pk})

class Payment(models.Model):
    account = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    account_number = models.CharField(max_length=12, null=True, blank=True, validators=[
        RegexValidator(r'^\d{1,12}$')])
    bank = models.CharField(
        max_length=255, null=True, blank=True)
    account_name = models.CharField(
        max_length=255, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    otp = models.CharField(
        max_length=255, blank=False, null=False)
    amount = models.IntegerField(blank=False, null=False)
    receiver_email = models.EmailField(blank=True)
    routing_number = models.CharField(max_length=255, blank=True, null=True)
    bank_address = models.CharField(max_length=255, blank=True, null=True)
    remark = models.CharField(max_length=255, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('bank:payment-list', kwargs={'pk': self.pk})
    

class Bank(models.Model):
    bank_fullname = models.CharField(
        max_length=255, null=True, blank=True)
    bank_abbr = models.CharField(
        max_length=255, null=True, blank=True)
    
    bank_logo = CloudinaryField('image', null=True, blank=True)

    class Meta:
        ordering = ['bank_fullname']

    def __str__(self):
        return f'{self.bank_fullname}'
    
class CardType(models.Model):
    company_name = models.CharField(max_length=200, null=True, help_text='E.g. Master Card')
    company_logo = CloudinaryField('image', null=True, blank=True)

    def __str__(self):
        return f'{self.company_name}'
class Card(models.Model):
    account = models.OneToOneField(
        Account, on_delete=models.SET_NULL, null=True)
    
    card_number = models.CharField(max_length=16, validators=[RegexValidator(r'^\d{1,16}$')], unique=True, help_text='Card number should be 16 digits')
    expiry_date = models.DateField()
    card_type = models.ForeignKey(CardType, on_delete=models.SET_NULL, null=True)
    cvv = models.PositiveIntegerField(validators=[MaxValueValidator(999)], help_text='CVV should be 3 digits')

    def get_absolute_url(self):
        return reverse('bank:my_cards', kwargs={'pk': self.pk})


class Loan(models.Model):
    email = models.EmailField()
    phone_number = models.CharField(max_length=14, null=True)
    amount = models.PositiveIntegerField()