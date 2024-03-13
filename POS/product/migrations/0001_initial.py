# Generated by Django 4.2.6 on 2024-02-13 07:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('suppliers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True, unique=True)),
                ('code', models.CharField(max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Stock_Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new_quantity_recieved', models.IntegerField(blank=True, null=True)),
                ('available_quantity', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True, unique=True)),
                ('code', models.CharField(max_length=100, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True, unique=True)),
                ('shorthand', models.CharField(max_length=50, null=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product_Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, null=True, unique=True)),
                ('name', models.CharField(max_length=100, null=True, unique=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('cost_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('selling_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('profit_margin', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('markup', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('minimum_stock_level', models.IntegerField(blank=True, null=True)),
                ('expiry_date', models.DateField(blank=True, null=True)),
                ('product_image', models.ImageField(blank=True, null=True, upload_to='product_images/')),
                ('barcode', models.ImageField(blank=True, null=True, upload_to='product_barcode/')),
                ('location', models.CharField(max_length=20, null=True)),
                ('available_quantity', models.PositiveIntegerField(default=0, null=True)),
                ('available_package_quantity', models.PositiveIntegerField(default=0, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.category')),
                ('item_unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.unit')),
                ('subcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.subcategory')),
                ('supplier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='suppliers.supplier')),
            ],
        ),
        migrations.CreateModel(
            name='Package',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_products_item', models.IntegerField(blank=True, null=True)),
                ('package_name', models.CharField(max_length=100, null=True, unique=True)),
                ('cost_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('selling_price', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('available_quantity', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product_item')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product.unit')),
            ],
        ),
    ]
