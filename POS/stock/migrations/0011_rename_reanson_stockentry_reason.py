# Generated by Django 4.2.6 on 2023-11-18 01:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stock', '0010_stockentry_reanson_delete_receivedstock'),
    ]

    operations = [
        migrations.RenameField(
            model_name='stockentry',
            old_name='reanson',
            new_name='reason',
        ),
    ]
