#coding:utf-8
from django.db import models



# Create your models here.

#电影信息表
class MovieInfo(models.Model):

	movie_id = models.CharField('电影编号', max_length=10, primary_key=True)
	movie_title = models.CharField('电影名称', max_length=100)
	movie_type = models.CharField('电影类型', max_length=50, default='#')
	movie_ctr = models.CharField('制片国家', max_length=20, default='#')
	movie_lan = models.CharField('语言', max_length=20, default='#')
	movie_date = models.CharField('上映日期', max_length=30, default='#')
	movie_time = models.CharField('片长', max_length=10, default='#')
	movie_intro = models.TextField('剧情简介', default='#')
	movie_pic = models.CharField('图片链接', default='#', max_length=150)
	movie_dir = models.CharField('导演', default='#', max_length=30)
	movie_big_pic = models.CharField('大图', default='#', max_length=150)

	def __str__(self):
		return self.movie_title

#基于物品推荐数据表在数据库中做二级缓存
class ItemRec(models.Model):

	movie_id = models.CharField(max_length=10, primary_key=True)
	item_rec = models.CharField(max_length=120)

	def __str__(self):
		return self.movie_id

#基于用户推荐数据表在数据库中做二级缓存
class UserRec(models.Model):

	user_id = models.CharField(max_length=10, primary_key=True)
	user_rec = models.CharField(max_length=120)

	def __str__(self):
		return self.user_id

#用户历史评分数据记录表
class HistoricalData(models.Model):

	user_id = models.CharField(max_length=10)
	movie_id = models.CharField(max_length=20)
	ratings = models.IntegerField()
	timestamp = models.CharField(max_length=20)

	def __str__(self):
		return self.user_id

#个人信息表
class User(models.Model):

	user_id = models.CharField(max_length=10, primary_key=True)
	email = models.EmailField(max_length=70, blank=True)
	psw = models.CharField(max_length=20, blank=True)

	def __str__(self):
		return self.email

#用户行为记录表
class UserRecords(models.Model):

	records = models.CharField(max_length=10, primary_key=True)
	user_id = models.CharField(max_length=10, default='#')
	click_date = models.CharField(max_length=10, default='#')
	click_movie = models.CharField(max_length=10, default='#')
	interest = models.CharField(max_length=2, default='#')
	click_times = models.CharField(max_length=2, default='#')

	def __str__(self):
		return self.user_id
