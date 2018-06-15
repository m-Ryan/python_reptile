from django.db import models

class ArticleModel(models.Model):
    title = models.CharField("标题", max_length=30)
    writer = models.CharField("作者", max_length=30)
    content = models.TextField("文章内容", )
    source = models.CharField("来源", max_length=30)
    date = models.CharField("日期", max_length=100)
    tagId = models.IntegerField("类型id" )
    tagName = models.CharField("类型名称", max_length=15)
    img = models.CharField("文章图片", max_length=255)
    cutImg = models.CharField("文章缩略图", max_length=255)