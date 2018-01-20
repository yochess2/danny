# Generated by Django 2.0.1 on 2018-01-20 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=63),
        ),
        migrations.AlterField(
            model_name='listing',
            name='title',
            field=models.CharField(max_length=127),
        ),
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('active', 'title')},
        ),
        migrations.AlterUniqueTogether(
            name='listing',
            unique_together={('active', 'title')},
        ),
    ]
