# Generated by Django 4.2.6 on 2024-02-13 07:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(max_length=100, null=True)),
                ('amount_paid', models.DecimalField(decimal_places=2, default=0, max_digits=5, null=True)),
                ('change', models.DecimalField(decimal_places=2, default=0, max_digits=5, null=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_cost_price', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('total_quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('discount', models.DecimalField(decimal_places=2, default=0, max_digits=5, null=True)),
                ('invoice_number', models.CharField(blank=True, null=True)),
                ('sale_number', models.CharField(blank=True, max_length=12, null=True)),
                ('date_created', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.CharField(max_length=20, null=True)),
                ('sub_total_cost_price', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('total_gross_profit', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_item', to='sales.paymentdetails')),
            ],
        ),
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SaleProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(blank=True, null=True)),
                ('cost_unit_price', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('profit', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('total_cost_price', models.DecimalField(decimal_places=2, max_digits=20, null=True)),
                ('package_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='product.package')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product_item')),
                ('sale', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='sales.sale')),
            ],
        ),
        migrations.AddField(
            model_name='sale',
            name='products',
            field=models.ManyToManyField(through='sales.SaleProduct', to='product.product_item'),
        ),
        migrations.AddField(
            model_name='sale',
            name='tax',
            field=models.ManyToManyField(related_name='sale_tax', to='sales.tax'),
        ),
        migrations.CreateModel(
            name='PausedSale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False, null=True)),
                ('sale', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='sales.sale')),
            ],
        ),
    ]
