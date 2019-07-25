# -*- coding:utf-8 -*-


import requests
from lxml import etree
import time
import re
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE","recSystem.settings")
import django
django.setup()
import time
import urllib

from rec.models import MovieInfo

__Author__='ZYQ'
file_path='/home/ubuntu/GraduationProject/Spark/resource/movie_title.txt'
movie_title_list=[]
movie_info_list=[]


class movie_spider:
    def get_html_text(self,url):
        try:
            headers={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3371.0 Safari/537.36',
                     'Cookie':'bid=bUVjzAybDLc; ll="108258"; ct=y; viewed="1084336"; __utmc=30149280; __utmz=30149280.1521387847.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=223695111; __utmz=223695111.1521387847.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); _vwo_uuid_v2=DA221DC69E86272FD61786E3A30BBBE6D|9709f94cba26a05e1fe04923feee6e70; ps=y; dbcl2="175532472:VjLHS+DU/cg"; ck=hOyE; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=6bb8b94c76be2058.1521387847.2.1521429133.1521388685.; _pk_ses.100001.4cf6=*; __utma=30149280.845038796.1521387847.1521387847.1521429133.2; __utmb=30149280.0.10.1521429133; __utma=223695111.309988786.1521387847.1521387847.1521429133.2; __utmb=223695111.0.10.1521429133',}
            r = requests.get(url=url,timeout=30,headers=headers)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            return r.text
        except:
            return 'error_in_getHTMLtext'

    def get_movie_id(self,html):
        try:
            # s = etree.HTML(html)
            # content = s.xpath('/html/body/div[2]/div/div/ul/li[2]/ul/li[1]/a/@href')
            # return(content[0].split("/")[3])
            subject_number = re.search('movie/subject/.*/',html).group(0).split('/')[2]
            return subject_number
        except:
            print('error_in_movie_id')
            pass

    def get_movie_detail(self,html,num,title):
        s = etree.HTML(html)
        try:
            movie_title = s.xpath('//*[@id="content"]/h1/span[1]/text()')
            movie_type = s.xpath('//*[@id="info"]/*[@property="v:genre"]/text()')
            movie_date = s.xpath('//*[@id="info"]/*[@property="v:initialReleaseDate"]/@content')
            movie_runtime = s.xpath('//*[@id="info"]/*[@property="v:runtime"]/@content')
            movie_lan = re.search(' .*',re.search('语言:<.*>.*<',html).group(0)).group(0)[:-1].strip()
            movie_ctr =re.search(' .*',re.search('制片国家/地区:<.*>.*<',html).group(0)).group(0)[:-1].strip()
            movie_pic = s.xpath('//*[@id="mainpic"]/a/img/@src')[0]
            movie_dir = s.xpath('//*[@id="info"]/span[1]/span[2]/a[@rel="v:directedBy"]/text()')[0]
            movie_big_pic = self.get_big_pic(s.xpath('//*[@id="mainpic"]/a[@class="nbgnbg"]/@href')[0])
            movie_intro = self.get_intro(s)

            movie_runtime = self.check_runtime(movie_runtime,html)

            MovieInfo.objects.create(movieId = num,movieTitle = movie_title,movie_type =movie_type,movie_date = movie_date,movie_time = movie_runtime,movie_lan =movie_lan,movie_ctr =movie_ctr,movie_pic =movie_pic,movie_dir =movie_dir,movie_big_pic = movie_big_pic, movie_intro = movie_intro)

        except:
            print("error_in_movie_detail")
            MovieInfo.objects.create(movieId =num,movieTitle=title)

    def check_runtime(self,runtime,html):
        try:
            if runtime == []:
                return re.search(' .*分钟',re.search('单集片长:<.*>.*<',html).group(0)).group(0).strip()
            else:
                return runtime
        except:
            return []

    def get_intro(self,s):
        flag = -1
        parse_method = ['//*[@id="link-report"]/span[@class="all hidden"]/text()','//*[@id="link-report"]/span[@property="v:summary"]/text()']
        for i in range(len(parse_method)):
            item = s.xpath(parse_method[i])
            if item == []:
                continue
            else:
                flag = i
        if flag == -1:
            return []
        else:
            return s.xpath(parse_method[flag])[0].strip()

    def get_big_pic(self,url):
        try:
            html = self.get_html_text(url)
            s = etree.HTML(html)
            big_pic_html = etree.HTML(self.get_html_text(s.xpath('//*[@id="content"]/div/div[1]/ul/li[1]/div[1]/a/@href')[0]))
            return big_pic_html.xpath('//*[@id="content"]/div/div[1]/div[2]/div/a[1]/img/@src')
        except:
            return '#'

def get_movie_list(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.readlines()

def main():
    # search_url = 'https://m.douban.com/search/?query={}'
    search_url = 'https://m.douban.com/search/?'
    detail_url = 'https://movie.douban.com/subject/{}/'
    spider=movie_spider()
    movie_title_list = get_movie_list(file_path)

    dic = {}
    for i in range(len(movie_title_list)):
        print('\r正在爬取第{}条数据'.format(str(i+1)))
        dic['query'] = movie_title_list[i]
        # movie_title_item = movie_title_list[i].replace(' ','+')
        search_html = spider.get_html_text(search_url + urllib.parse.urlencode(dic))
        movie_id = spider.get_movie_id(search_html)
        detail_html = spider.get_html_text(detail_url.format(str(movie_id)))
        spider.get_movie_detail(detail_html,str(i+1),str(movie_title_list[i]))
        time.sleep(1)
if __name__ == '__main__':
    main()
