# Generated by Django 4.2.6 on 2023-12-16 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suppliers', '0002_alter_supplier_opening_balance'),
        ('purchases', '0014_alter_purchaseorder_discount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='suppliers.supplier'),
        ),
        migrations.DeleteModel(
            name='ReceivedProductHistory',
        ),
    ]
