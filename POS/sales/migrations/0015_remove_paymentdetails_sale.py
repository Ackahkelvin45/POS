# Generated by Django 4.2.6 on 2023-12-02 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0014_alter_paymentdetails_sale'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paymentdetails',
            name='sale',
        ),
    ]
