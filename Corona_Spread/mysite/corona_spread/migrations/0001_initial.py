# Generated by Django 3.0.5 on 2020-04-09 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Global_Cases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=50)),
                ('cases', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Hospital_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=50)),
                ('hosp_num', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Temp_Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=50)),
                ('avg_temp', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='US_Cases',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=50)),
                ('cases', models.IntegerField(default=0)),
                ('deaths', models.IntegerField(default=0)),
            ],
        ),
    ]
