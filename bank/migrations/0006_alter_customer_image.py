# Generated by Django 4.1.1 on 2022-09-16 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0005_alter_customer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(default='avatar/avatar.png', upload_to='avatar'),
        ),
    ]
