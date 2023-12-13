# Generated by Django 4.2.6 on 2023-11-16 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchases', '0009_purchaseorder_received_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseorder',
            name='received_quantity',
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='received_quantity',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]
