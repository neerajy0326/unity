# Generated by Django 4.1.10 on 2023-08-16 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='account_type',
            field=models.CharField(choices=[('savings', 'Savings Account'), ('checking', 'Checking Account'), ('credit', 'Credit Card')], default='none', max_length=20),
        ),
        migrations.AddField(
            model_name='customuser',
            name='contact_number',
            field=models.CharField(default='none', max_length=15),
        ),
        migrations.AddField(
            model_name='customuser',
            name='date_of_birth',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('prefer_not_to_say', 'Prefer not to say')], default='none', max_length=20),
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
