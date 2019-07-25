import re
import time
import os
import xlrd
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GraduationProject.settings")

import django
django.setup()

from Spark.models import MovieInfo


def importData(fpath):
	workbook = xlrd.open_workbook(fpath)
	booksheet = workbook.sheet_by_name('Sheet1')
	count = 0
	for i in range(1, booksheet.nrows):
		item = booksheet.row_values(i)
		MovieInfo.objects.create(movie_id = int(item[5]), movie_title = item[10], movie_type = item[11], movie_ctr = item[2], movie_lan = item[7], movie_date = item[3], movie_time = item[9], movie_intro = item[6], movie_pic = item[8], movie_dir = item[4], movie_big_pic = item[1])
		count += 1
		print('\r当前进度: {:.2f}%'.format(count * 100 / booksheet.nrows), end="")
		
def main():
	fpath = '/home/ubuntu/GraduationProject/Spark/resource/movie_data.xlsx'
	importData(fpath)

main()
