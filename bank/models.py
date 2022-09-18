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
    CUSTOMER_ID = models.CharField(max_length=255, null=True)
    # first_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    # last_name = models.CharField(max_length=255, null=True)
    SSN = USSocialSecurityNumberField(max_length=9)
    mobile_number = PhoneNumberField()
    # email_address = models.EmailField(max_length=254, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    # image = models.ImageField(default='avatar.png', upload_to='avatar')
    image = CloudinaryField('image')
    email_confirmed = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'{self.user.first_name} {self.middle_name} {self.user.last_name}'

    def account_name(self):
        return f'{self.user.first_name} {self.middle_name} {self.user.last_name}'

    def get_absolute_url(self):
        return reverse('bank:customer-update', kwargs={'pk': self.pk})

    account_name.short_description = 'Customer'


class Account(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    # balance = models.IntegerField(blank=True, null=True)
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
    created_on = models.DateTimeField(auto_now_add=True)

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
    account_number = models.CharField(max_length=12, null=True, blank=True, validators=[
        RegexValidator(r'^\d{1,12}$')])
    bank = models.CharField(
        max_length=255, null=True, default='Cadence')
    account_name = models.CharField(
        max_length=255, blank=True, null=True)
    date = models.DateField(auto_now_add=True)
    amount = models.IntegerField(blank=False, null=False)
    error_message = models.TextField(blank=True)

    def get_absolute_url(self):
        return reverse('bank:posttransactions-list', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-date']


class Payment(models.Model):
    account = models.ForeignKey(
        Account, on_delete=models.SET_NULL, null=True, blank=True)
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

    # def get_throttle_factor(self):
    #     return settings.OTP_EMAIL_THROTTLE_FACTOR

    # def generate_challenge(self, extra_context=None):
    #     """
    #     Generates a random token and emails it to the user.

    #     :param extra_context: Additional context variables for rendering the
    #         email template.
    #     :type extra_context: dict

    #     """
    #     self.generate_token(valid_secs=settings.OTP_EMAIL_TOKEN_VALIDITY)

    #     context = {'token': self.token, **(extra_context or {})}
    #     if settings.OTP_EMAIL_BODY_TEMPLATE:
    #         body = Template(settings.OTP_EMAIL_BODY_TEMPLATE).render(
    #             Context(context))
    #     else:
    #         body = get_template(
    #             settings.OTP_EMAIL_BODY_TEMPLATE_PATH).render(context)

    #     send_mail(settings.OTP_EMAIL_SUBJECT,
    #               body,
    #               settings.OTP_EMAIL_SENDER,
    #               [self.account.customer.user.email])

    #     message = "sent by email"

    #     return message

    # def verify_token(self, token):
    #     verify_allowed, _ = self.verify_is_allowed()
    #     if verify_allowed:
    #         verified = super().verify_token(token)

    #         if verified:
    #             self.throttle_reset()
    #         else:
    #             self.throttle_increment()
    #     else:
    #         verified = False

    #     return verified

    # class Meta:
    #     ordering = ['-date']
