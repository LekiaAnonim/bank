# Generated by Django 4.1.1 on 2022-09-12 21:03

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import localflavor.us.models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(choices=[('Checking', 'Checking'), ('Savings', 'Savings'), ('Time Deposit', 'Time Deposit'), ('Personal Loan', 'Personal Loan'), ('Credit Line', 'Credit Line'), ('DH Real Estate Loan', 'DH Real Estate Loan'), ('Business Loan', 'Business Loan'), ('Real Estate Loan', 'Real Estate Loan')], max_length=300, null=True)),
                ('account_number', models.CharField(max_length=12, null=True, unique=True, validators=[django.core.validators.RegexValidator('^\\d{1,12}$')])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['account_type', 'created_on'],
            },
        ),
        migrations.CreateModel(
            name='PostTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,12}$')])),
                ('bank', models.CharField(default='Cadence', max_length=255, null=True)),
                ('account_name', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('amount', models.IntegerField()),
                ('error_message', models.TextField(blank=True)),
                ('account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bank.account')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_number', models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.RegexValidator('^\\d{1,12}$')])),
                ('bank', models.CharField(blank=True, default='Cadence', max_length=255, null=True)),
                ('account_name', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('otp', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('receiver_email', models.EmailField(blank=True, max_length=254)),
                ('routing_number', models.CharField(blank=True, max_length=255, null=True)),
                ('bank_address', models.CharField(blank=True, max_length=255, null=True)),
                ('account', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='bank.account')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CUSTOMER_ID', models.CharField(max_length=255, null=True)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('SSN', localflavor.us.models.USSocialSecurityNumberField(max_length=11)),
                ('mobile_number', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(default='avatar.png', upload_to='avatar')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
        migrations.AddField(
            model_name='account',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='bank.customer'),
        ),
    ]
