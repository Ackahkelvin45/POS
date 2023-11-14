# Generated by Django 4.2.6 on 2023-11-13 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('purchases', '0006_alter_purchaseorder_invoice_number'),
        ('product', '0009_alter_product_item_barcode'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceivedStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_quantity', models.PositiveIntegerField(default=0)),
                ('received_at', models.DateField(auto_now_add=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product_item')),
                ('purchase_order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='purchases.purchaseorder')),
            ],
        ),
    ]
