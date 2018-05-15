# -*- coding: utf8 -*-
from django.db import models

# Create your models here.
class Book(models.Model):
  # 書名
  title = models.CharField(max_length=255)
  # 作者
  author = models.CharField(max_length=255)


# 讀者
class Reader(models.Model):
  # 姓名
  realname = models.CharField(max_length=255)
  # 連絡電話
  phone = models.CharField(max_length=255)


# 流通紀錄
class Circulation(models.Model):
  # 書籍 
  book = models.ForeignKey(Book)
  # 借閱人
  reader = models.ForeignKey(Reader)
  # 借出日期
  date_checkout = models.DateField(blank=False)
  # 歸還日期, 若為 null 表示尚未歸還
  date_return = models.DateField(null=True)