# Generated by Django 4.1.1 on 2023-06-03 21:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0029_alter_currency_currency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='bank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]