# Generated by Django 4.1.10 on 2023-08-16 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_customuser_pin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='ifsc',
            field=models.CharField(blank=True, max_length=5, null=True),
        ),
    ]