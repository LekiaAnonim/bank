# Generated by Django 4.1.1 on 2022-09-16 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0006_alter_customer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='image',
            field=models.ImageField(default='avatar.png', upload_to='avatar'),
        ),
    ]