# Generated by Django 4.1.1 on 2022-10-06 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0013_remove_customer_customer_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posttransaction',
            name='account_name',
        ),
        migrations.RemoveField(
            model_name='posttransaction',
            name='account_number',
        ),
        migrations.AlterField(
            model_name='account',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bank.customer'),
        ),
    ]