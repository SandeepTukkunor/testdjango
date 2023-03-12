# Generated by Django 4.0.10 on 2023-03-12 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=256, null=True)),
                ('last_name', models.CharField(blank=True, max_length=256, null=True)),
                ('dob', models.DateTimeField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=256, null=True)),
            ],
        ),
    ]
