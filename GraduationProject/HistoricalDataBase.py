import re
import time 
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GraduationProject.settings")

import django
django.setup()

def importData(fpath):
	with open(fpath, 'r') as f1:
		from Spark.models import HistoricalData
		ls = []
		count = 0
		for item in f1.readlines():
			ls.append(item.strip().split('\t'))
		for i in range(len(ls)):
			if len(ls[i])<4:
				ls.pop(i)
			HistoricalData.objects.create(user_id=ls[i][0], movie_id=ls[i][1], ratings=ls[i][2], timestamp=ls[i][3])
			count += 1
			print('\r当前进度: {:.2f}%'.format(count * 100 / len(ls)), end="")

def main():
	path = '/home/ubuntu/GraduationProject/Spark/resource/u.data'
	importData(path)

main()
