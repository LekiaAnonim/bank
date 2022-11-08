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
    date = models.DateField(auto_now_add=True)
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


class Payment(models.Model):
    account = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True)
    account_number = models.CharField(max_length=12, null=True, blank=True, validators=[
        RegexValidator(r'^\d{1,12}$')])
    bank = models.CharField(
        max_length=255, null=True, blank=True, default='Cadence')
    account_name = models.CharField(
        max_length=255, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    otp = models.CharField(
        max_length=255, blank=False, null=False)
    amount = models.IntegerField(blank=False, null=False)
    receiver_email = models.EmailField(blank=True)
    routing_number = models.CharField(max_length=255, blank=True, null=True)
    bank_address = models.CharField(max_length=255, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('bank:payment-list', kwargs={'pk': self.pk})