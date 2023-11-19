# Generated by Django 4.1.1 on 2022-10-15 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0019_alter_payment_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='block_account_message',
            field=models.TextField(default='This account has been blocked Kindly contact the administrator to learn more Or enter a valid username and password.'),
        ),
        migrations.AddField(
            model_name='account',
            name='suspend_account_message',
            field=models.TextField(default='This account has been suspended Kindly contact the administrator to learn more Or enter a valid username and password.'),
        ),
    ]
