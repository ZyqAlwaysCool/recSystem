import re
import time
import os
import xlrd
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GraduationProject.settings')

import django
django.setup()

from Spark.models import UserRec as UR
from Spark.models import ItemRec as IR
from Spark.models import User as U


def importData(fpath):
	workbook = xlrd.open_workbook(fpath)
	sheet0 = workbook.sheet_by_index(0)
	end = sheet0.nrows
	for i in range(0, end):
		item = sheet0.row_values(i)[0].strip('[').strip(']').split(',')
		u_rec = []
		u_id = re.search('[0-9]+', item[0]).group(0)
		for j in range(1, len(item)):
			u_rec.append(re.search('[0-9]+', item[j]).group(0))
		UR.objects.create(user_id=u_id, user_rec=u_rec)
		#IR.objects.create(movie_id=u_id, item_rec=u_rec)
		print('第{}条已完成'.format(i))

def importUserData(fpath):
	workbook = xlrd.open_workbook(fpath)
	sheet0 = workbook.sheet_by_index(0)
	end = sheet0.nrows
	for i in range(0, end):
		U.objects.create(user_id=sheet0.row_values(i)[0].strip('[').strip(']').replace('\'', ''), email='#', psw='#')
		print('第{}条已完成'.format(i))

def main():
	path = '/home/ubuntu/GraduationProject/Spark/resource/user_rec.xls'
	path1 = '/home/ubuntu/GraduationProject/Spark/resource/user_info.xls'
	#importData(path)
	importUserData(path1)

	
main()
