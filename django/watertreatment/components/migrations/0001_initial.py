# Generated by Django 4.1.3 on 2023-03-13 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('elemID', models.IntegerField(blank=True, db_column='elemID', primary_key=True, serialize=False)),
                ('name', models.TextField(blank=True, null=True)),
                ('params', models.TextField(blank=True, null=True)),
            ],
            options={
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='SimDataTable',
            fields=[
                ('components', models.TextField(blank=True, db_column='components', primary_key=True, serialize=False)),
                ('snapshots', models.IntegerField(blank=True, null=True)),
                ('waterLevel', models.IntegerField(blank=True, null=True)),
                ('sanddisp', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'managed': False,
            },
        ),
    ]
