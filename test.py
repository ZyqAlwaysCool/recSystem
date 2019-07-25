from pyspark import SparkConf, SparkContext
import pyspark.mllib.recommendation as rd
import redis
from kafka import KafkaConsumer

APP_NAME = 'My Spark Application'
path = '/home/ubuntu/data/u.data'
if_no_rec_data = [1449, 1398, 119, 1642, 1594, 408, 318, 169, 483, 114]


def data_from_kafka(topic_name):
	consumer = KafkaConsumer(topic_name, bootstrap_servers=['localhost:9092'], auto_offset_reset='smallest')
	#写入评分数据
	for i in consumer:
		temp = []
		item = bytes.decode(i.value).split(',')
		timestamp = i.timestamp
		f1 = open(path, 'a')
		f1.write('\n{}\t{}\t{}\t{}'.format(item[0], item[1], item[2], str(timestamp)))
		f1.close()

def get_rating(str):
	arr = str.split('\t')
	user_id = int(arr[0])
	movie_id = int(arr[1])
	user_rating = float(arr[2])
	return rd.Rating(user_id, movie_id, user_rating)

#测试als结果用
def test_als(recs, userid):
	print('------rec_data_for_user{}------'.format(userid))
	for movie in recs:
		print(movie.product)
	print('------finished_rec------')

#获得用户编号
def get_rec_user(path):
	user = []
	with open(path, 'r') as f:
		for i in f:
			user.append(i.split('\t')[0])
	return set(user)


def als(path, user_set):
	#data_from_kafka('trainMsg')
	rawData = sc.textFile(path)#读取文件
	ratings = rawData.map(get_rating)#评分矩阵
	model = rd.ALS.train(ratings, 50, 10, 0.01)#训练模型
	#产生用户喜好推荐数据
	for user in user_set:
		try:
			topKRecs = model.recommendProducts(int(user), 10)
			rec_lst = []
			for item in topKRecs:
				rec_lst.append(item.product)
				data_to_redis(rec_lst, user)
		except:
			data_to_redis(if_no_rec_data, user)
	print('----finished_rec----')

def data_to_redis(datas, userid):
	r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
	r.set(userid, str(datas), ex=600)

def main(sc):
	user = get_rec_user(path)
	print('----user_set_len:{}----'.format(len(user)))
	als(path, user)

if __name__ == "__main__":
	conf = SparkConf().setAppName(APP_NAME)
	conf = conf.setMaster("local[*]")
	sc = SparkContext(conf = conf)

	main(sc)
