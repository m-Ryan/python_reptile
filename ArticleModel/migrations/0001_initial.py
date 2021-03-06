# Generated by Django 2.0.6 on 2018-06-14 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ArticleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='标题')),
                ('writer', models.CharField(max_length=30, verbose_name='作者')),
                ('content', models.TextField(verbose_name='文章内容')),
                ('source', models.CharField(max_length=30, verbose_name='来源')),
                ('date', models.CharField(max_length=100, verbose_name='日期')),
                ('tagId', models.IntegerField(verbose_name='类型id')),
                ('tagName', models.CharField(max_length=15, verbose_name='类型名称')),
                ('img', models.CharField(max_length=255, verbose_name='文章图片')),
                ('cutImg', models.CharField(max_length=255, verbose_name='文章缩略图')),
            ],
        ),
    ]
