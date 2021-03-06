# Generated by Django 2.0.5 on 2018-06-20 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_time', models.DateTimeField(auto_now=True, verbose_name='访问时间')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='book.ISBNBook', verbose_name='访问书籍')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='login.User', verbose_name='访问用户')),
            ],
            options={
                'verbose_name': '访问记录',
                'verbose_name_plural': '访问记录',
                'ordering': ['id'],
            },
        ),
    ]
