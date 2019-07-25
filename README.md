## recSystem-demo

### 前端
* bootstrap

### 后端
* django
* spark

### 中间件
* kafka
* redis

### 所需软件
* redis
* kafka
* zookeeper
* spark

### 监听端口
* redis:6379 redis-cli
* zookeeper:2181
* kafka:9092

### 常用命令
* 检查服务器运行状态:`netstat -nlt|grep 端口`
* 检查zookeeper:`telnet localhost 2181` anwser:ruok->im ok
* 启动spark推荐服务:`./bin/spark-submit /home/ubuntu/test.py`
* 命令行启动kafka:.`/bin/kafka-server-start.sh config/server.properties`
* 消费kafka中的topic: `~/kafka/kafka_2.11-1.0.0/bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic test_topic --from-beginning`
* python消费kafka中数据:`consumer = KafkaConsumer("topic",bootstrap_servers=['localhost:9092'], auto_offset_reset='smallest')`
* auto_offset_reset='smallest'表示重置队列偏移量，类似于--from-beginning

### spark服务
test.py文件中
