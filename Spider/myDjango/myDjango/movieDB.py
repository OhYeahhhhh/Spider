import requests
from lxml import etree
import MySQLdb
import re

def get_page(start_num):
    url="https://movie.douban.com/top250?start=%s&filter=" %start_num
    res=requests.get(url)
    tree=etree.HTML(res.text)
    title=tree.xpath('//span[@class="title"][1]/text()')
    print(title)
    return title

def get_all_page(start,end):
    result=[]
    for i in range(start,end-start):
        title_list=get_page(i*25)
        result+=title_list
    return result

conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='scraping', charset="utf8")
cur=conn.cursor()

def check_table(table_name):
    sql = "SELECT count(*) FROM information_schema.TABLES WHERE table_name ='%s';" %table_name
    count = cur.execute(sql)
    if count==1:
        return True
    else:
        return False

def insertDB():
    result=get_all_page(0,10)
    if check_table('myApp_movies'):
        cur.execute('delete from myApp_movies')
    for i in range(len(result)):
        mName=result[i]
        mId=i+1
        cur.execute("insert into myApp_movies(mId,mName)values(%s,%s)",(mId,mName))
    cur.close()
    conn.commit()
    conn.close()
    print("数据添加成功！")

if __name__ == "__main__":
    insertDB()


