# Generated by Django 2.2.6 on 2020-08-01 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('p_library', '0009_auto_20200801_0828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='book_img',
            field=models.ImageField(blank=True, null=True, upload_to='book_cover/'),
        ),
    ]
