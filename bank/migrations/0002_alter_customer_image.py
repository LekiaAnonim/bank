# Generated by Django 4.1.1 on 2022-09-15 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(default='bank/static/avatar.png', upload_to='avatar'),
        ),
    ]
