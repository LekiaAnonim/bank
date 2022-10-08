# Generated by Django 4.1.1 on 2022-10-08 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0014_remove_posttransaction_account_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='posttransaction',
            name='top_up_type',
            field=models.CharField(choices=[('Credit', 'Credit'), ('Debit', 'Debit')], max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='posttransaction',
            name='date',
            field=models.DateField(),
        ),
    ]