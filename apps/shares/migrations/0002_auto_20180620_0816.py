# Generated by Django 2.0.5 on 2018-06-20 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shares', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='book.ISBNBook', verbose_name='分享书籍'),
        ),
    ]
