#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from Spark.models import *
from django.core.cache import cache
import json
import random
import time
import re
from datetime import date as dt
import redis
from kafka import KafkaProducer
from kafka import KafkaConsumer


response_string = 'successCallback({});'

def zyq(request):
	return HttpResponse('long time no see, zyq:)')


#数据进消息队列
@csrf_exempt
def sendMsg(topic, content):
	try:
		producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
		producer.send(topic, content)
	except:
		pass

#从redis取出消息
@csrf_exempt
def getMsgFromRedis(Id):
	r = redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)
	if str(r.get(Id)) == 'None':
		return 'None'
	else:
		recList = r.get(Id)[1:-1].replace('\'', '').replace(' ', '').split(',')
		return recList

#从数据库取出物品推荐数据
@csrf_exempt
def getItemRecDataFromDB(Id):
	itemRecRaw = ItemRec.objects.get(movie_id = Id).item_rec
	itemRecLst = itemRecRaw[1:-1].replace('\'', '').replace(' ', '').split(',')
	return itemRecLst

#从数据库取出用户推荐数据
@csrf_exempt
def getUserRecDataFromDB(Id):
	userRecRaw = UserRec.objects.get(user_id = Id).user_rec
	userRecLst = userRecRaw[1:-1].replace('\'', '').replace(' ', '').split(',')
	return userRecLst

#从数据库取出电影信息
@csrf_exempt
def getMovieFromDB(recMovieIdLst):
	recMovieInfoLst = []
	for i in range(len(recMovieIdLst)):
		recMovieInfoDct = {}
		item = MovieInfo.objects.get(movie_id = str(recMovieIdLst[i]))
		recMovieInfoDct['id'] = item.movie_id
		recMovieInfoDct['title'] = item.movie_title
		recMovieInfoDct['dir'] = item.movie_dir
		recMovieInfoDct['pic'] = item.movie_pic
		recMovieInfoDct['intro'] = item.movie_intro
		recMovieInfoDct['type'] = item.movie_type
		recMovieInfoLst.append(recMovieInfoDct)
	recMovieInfo = json.dumps(recMovieInfoLst)
	return recMovieInfo

#随机抽取电影
@csrf_exempt
def returnRandomMovie(movieNum):
	movieCountLst = [n for n in range(1, 1683)]
	movieRandomLst = random.sample(movieCountLst, movieNum)
	recMovieInfo = getMovieFromDB(movieRandomLst)
	return recMovieInfo

#基于用户推荐应用逻辑
@csrf_exempt
def getUserRecMsg(request):
	if request.method == 'GET':
		userId = str(request.GET['usrId'])
		movieNum = 10
		recLst = []
		recType = {}
		recType['records'] = 'null'
		if userId != '*':
			userRecLst = getMsgFromRedis(userId)
			if userRecLst == 'None':
				userRecLst = getUserRecDataFromDB(userId)
			elif str(userRecLst) != getUserRecDataFromDB(userId):
				#redis与用户偏好推荐数据库数据不一致时将redis数据写入MySQL数据库
				u = UserRec.objects.get(user_id = userId)
				u.user_rec = str(userRecLst)
				u.save()
		else:
			userRecLst = []
		if UserRec.objects.filter(user_id = userId).count() == 0 or len(userRecLst) != 10:
			movie = [1449, 1398, 119, 1642, 1594, 408, 318, 169, 483, 114]
			rec = getMovieFromDB(movie)
			return HttpResponse(response_string.format(json.dumps({'recMovie':rec, 'records':recType['records']})))
		else:
			recMovieInfo = getMovieFromDB(userRecLst)
			return HttpResponse(response_string.format(json.dumps({'recMovie':recMovieInfo, 'records':'null'})))

#对电影打分
@csrf_exempt
def rateTheMovie(request):
	if request.method == 'GET':
		Msg = request.GET
		userId = str(Msg['usrId'])
		movieTitle = str(Msg['movieTitle'])
		ratings = str(Msg['ratings'])
		topic = ['trainMsg']
		movieId = str(getMovieIdFromDB(movieTitle))
		if movieId == 'Error_In_getMovieIdFromDB':
			return HttpResponse(response_string.format(json.dumps({"status":movieId})))
		userMsg = userId + ',' + movieId + ',' + ratings
		sendMsg(topic[0], bytes(userMsg, encoding='utf-8')) #向kafka传递数据
		if HistoricalData.objects.filter(user_id=userId, movie_id=movieId).count() != 0:
			record = HistoricalData.objects.get(user_id=userId, movieId=movieId)
			record.ratings = int(ratings)
			record.timeStamp = str(int(time.time()))
			record.save()
		else:
			HistoricalData.objects.create(user_id=userId, movie_id=movieId, ratings=int(ratings), timestamp=str(int(time.time())))
		return HttpResponse(response_string.format(json.dumps({"status":"success_rate_the_movie"})))
	else:
		return HttpResponse(response_string.format(json.dumps({"status":"request_method_error"})))

#从电影数据库取出电影编号
@csrf_exempt
def getMovieIdFromDB(movieTitle):
	try:
		item = MovieInfo.objects.filter(movie_title__contains = movieTitle)
		movieId = item[0].movie_id
		print(movieId)
		return movieId
	except:
		return 'Error_In_getMovieIdFromDB'

#获取基于物品推荐数据信息(此段逻辑有修改)
@csrf_exempt
def getItemRecMsg(request):
	if request.method == 'GET':
		Msg = request.GET
		movieTitle = str(Msg['movieTitle']).strip()
		print(movieTitle)
		movieIdFromDB = getMovieIdFromDB(movieTitle)
		if movieIdFromDB == 'Error_In_getMovieIdFromDB':
			return HttpResponse(movieIdFromDB)
		else:
			try:
				recMovieInfo = getMovieFromDB(getItemRecDataFromDB(movieIdFromDB))
				return HttpResponse(response_string.format(str(recMovieInfo)))
			except:
				return HttpResponse(response_string.format(json.dumps({"status":"no_similar_rec_movie"})))
	else:
		return HttpResponse(response_string.format(json.dumps({'request_Method_Error'})))

#获取历史评分数据
@csrf_exempt
def getHistoricalData(request):
	if request.method == 'GET':
		Msg = request.GET
		userId = str(Msg['usrId'])
		historicalDataDct = {'19':{}, '20':{}}
		countFor19 = 0
		countFor20 = 0
		for i in HistoricalData.objects.filter(user_id=userId).order_by('-timestamp'):
			movieTitle = MovieInfo.objects.get(movie_id=i.movie_id).movie_title
			ratings = str(i.ratings)
			timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(i.timestamp)))
			if re.search('19.*', timestamp):
				countFor19 += 1
				historicalDataDct['19'][str(countFor19)] = 'Movie:' + movieTitle + ' ' + 'Ratings:' + ratings + ' ' + 'Date:' + timestamp
			else:
				countFor20 += 1
				historicalDataDct['20'][str(countFor20)] = 'Movie:' + movieTitle + ' ' + 'Ratings:' + ratings + ' ' + 'Date:' + timestamp
		historicalDataByJson = json.dumps(historicalDataDct)
		return HttpResponse(response_string.format(historicalDataByJson))
	else:
		return HttpResponse(response_string.format({"status":"request_method_error"}))

#读取完整电影信息
@csrf_exempt
def getFullMovieInfo(request):
	if request.method == 'GET':
		Msg = request.GET
		movieInfoDct = {}
		movieId = str(Msg['movie_id'])
		item = MovieInfo.objects.get(movie_id = movieId)
		movieInfoDct['title'] = item.movie_title
		movieInfoDct['type'] = item.movie_type
		movieInfoDct['ctr'] = item.movie_ctr
		movieInfoDct['lan'] = item.movie_lan
		movieInfoDct['date'] = item.movie_date
		movieInfoDct['time'] = item.movie_time
		movieInfoDct['intro'] = item.movie_intro
		movieInfoDct['dir'] = item.movie_dir
		movieInfoDct['big_pic'] = item.movie_big_pic
		movieInfoDct['pic'] = item.movie_pic
		movieInfo = json.dumps(movieInfoDct)
		return HttpResponse(response_string.format(str(movieInfo)))
	else:
		return HttpResponse(response_string.format("request_method_error"))

#注册功能
@csrf_exempt
def register(request):
	if request.method == 'GET':
		Msg = request.GET
		userNum = int(User.objects.all().count())
		if User.objects.filter(email = str(Msg['email'])).count() != 0:
			return HttpResponse(response_string.format(json.dumps({"status":"email_exist"})))
		else:
			newUserId = userNum + 1
			User.objects.create(user_id = str(newUserId), email = str(Msg['email']))
			item = User.objects.get(user_id = newUserId)
			item.psw = str(Msg['psw'])
			item.save()
			return HttpResponse(response_string.format(json.dumps({"status":"registered", "usrId":newUserId})))
	else:
		return HttpResponse(response_string.format(json.dumps({"status":"request_method_error"})))

#登录功能
@csrf_exempt
def login(request):
	if request.method == 'GET':
		Msg = request.GET
		try:
			emailCheck = User.objects.filter(email = str(Msg['email']))
			if Msg['usr_id'] == '-1' and emailCheck.count() == 1:
				return HttpResponse(response_string.format(json.dumps({"status":"logged_email", "usr_id":emailCheck[0].user_id})))
			elif Msg['usr_id'] != '-1':
				return HttpResponse(response_string.format(json.dumps({"status":"logged_num"})))
		except:
			return HttpResponse(response_string.format(json.dumps({"status":"login_error"})))
	else:
		return HttpResponse(response_string.format("request_method_error"))

@csrf_exempt
def allMovie(request):
	if request.method == 'GET':
		Msg = request.GET
		ctr = Msg['ctr']
		mtype = Msg['type'].replace(' ', '+')
		page = Msg['page']
		pageNum = 10
		infoDct = {}
		if ctr == '-1' and mtype =='-1':
			movie = MovieInfo.objects.all()
			num = movie.count()
			mItem = movie[(int(page) - 1)*pageNum : int(page)*pageNum].values()
			infoDct['movie_info'] = list(mItem)
			infoDct['movie_num'] = str(num)
			return HttpResponse(response_string.format(json.dumps(infoDct)))
		elif ctr != '-1' and mtype == '-1':
			movie = MovieInfo.objects.filter(movie_ctr__contains = str(ctr))
			num = movie.count()
			mItem = movie[(int(page) - 1)*pageNum : int(page)*pageNum].values()
			infoDct['movie_info'] = list(mItem)
			infoDct['movie_num'] = str(num)
			return HttpResponse(response_string.format(json.dumps(infoDct)))
		elif ctr == '-1' and mtype != '-1':
			mtypeLst = mtype.split('+')
			if len(mtypeLst) == 1:
				movie = MovieInfo.objects.filter(movie_type__contains = str(mtypeLst[0]))
				num = movie.count()
				mItem = movie[(int(page) - 1)*pageNum : int(page)*pageNum].values()
				infoDct['movie_info'] = list(mItem)
				infoDct['movie_num'] = str(num)
				return HttpResponse(response_string.format(json.dumps(infoDct)))
			else:
				try:
					mItem = MovieInfo.objects.filter(movie_type__contains = str(mtypeLst[0]))
					movie = filterMovieInfo(mItem, mtypeLst, 1)
					num = movie.count()
					filterResult = movie[(int(page) - 1)*page_num : int(page)*pageNum].values()
					infoDct['movie_info'] = list(filterResult)
					infoDct['movie_num'] = str(num)
					return HttpResponse(response_string.format(json.dumps(infoDct)))
				except:
					return HttpResponse(response_string.format(json.dumps({"movie_info":[]})))
		elif ctr != '-1' and mtype != '-1':
			mtypeLst = mtype.split('+')
			try:
				if len(mtypeLst) == 1:
					movie = MovieInfo.objects.filter(movie_ctr__contains = str(ctr), movie_type__contains = mtypeLst[0])
					num = movie.count()
					mItem = movie[(int(page) - 1)*pageNum : int(page)*pageNum].values()
					infoDct['movie_info'] = list(mItem)
					infoDct['movie_num'] = str(num)
					return HttpResponse(response_string.format(json.dumps(infoDct)))
				else:
					mItem = MovieInfo.objects.filter(movie_ctr__contains = str(ctr), movie_type__contains = mtypeLst[0])
					movie = filterMovieInfo(mItem, mtypeLst, 1)
					num = movie.count()
					filterResult = movie[(int(page) - 1)*pageNum : int(page)*pageNum].values()
					infoDct['movie_info'] = list(filterResult)
					infoDct['movie_num'] = str(num)
					return HttpResponse(response_string.format(json.dumps(infoDct)))
			except:
				return HttpResponse(response_string.format(json.dumps({"movie_info":[]})))

@csrf_exempt
def filterMovieInfo(content, typeLst, i):
	content = content.filter(movie_type__contains = str(typeLst[i]))
	if i == len(typeLst) - 1:
		return content
	else:
		i += 1
		return filterMovieInfo(content, typeLst, i)

@csrf_exempt
def rank(request):
	rank = [1467, 1201, 814, 1293, 1599, 1189, 1500, 1536, 1653, 1122]
	movieRank = getMovieFromDB(rank)
	return HttpResponse(response_string.format(json.dumps({'rank':movieRank})))

@csrf_exempt
def records(request):
	return HttpResponse('checked')

@csrf_exempt
def favor(request):
	return HttpResponse('send_to_usr_records_topic')

@csrf_exempt
def home(request):
	return render(request, 'index.html')

@csrf_exempt
def all_movies(request):
	return render(request, 'allmovies.html')

@csrf_exempt
def rank_list(request):
	return render(request, 'ranklist.html')

@csrf_exempt
def single_movie_detail(request):
	return render(request, 'single_movie_detail.html')
