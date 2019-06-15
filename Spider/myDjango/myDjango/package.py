import requests
import re
import MySQLdb

def getHtmlText(url):
    try:
        r=requests.get(url,timeout=30)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        return ""

def parsePage(ilt,html):
    try:
        plt=re.findall(r'\"view_price\"\:\"[\d\.]*\"',html)
        tlt=re.findall(r'\"raw_title\"\:\".*?\"',html)
        for i in range(len(plt)):
            price=eval(plt[i].split(':')[1])
            title=eval(tlt[i].split(':')[1])
            ilt.append([price,title])
    except:
        print("")

def printGoodsList(ilt):
    tplt="{:4}\t{:8}\t{:16}"
    print(tplt.format("序号","价格","商品名称"))
    count=0
    for i in ilt:
        count=count+1
        print(tplt.format(count,i[0],i[1]))

def main():
    goods='书包'
    depth=2
    start_url='https://s.taobao.com/search?q='+goods
    infoList=[]
    for i in range(depth):
        try:
            url=start_url+'&s='+str(44*i)
            html=getHtmlText(url)
            parsePage(infoList,html)
        except:
            continue
    printGoodsList(infoList)

    conn=MySQLdb.connect(host='localhost',user='root',passwd='123456',db='scraping', charset="utf8")
    cur=conn.cursor()
    for i in range(len(infoList)):
        cur.execute("insert into myapp_packages(pPrice,pTitle)values(%s,%s)",(infoList[i][0],infoList[i][1]))
    cur.close()
    conn.commit()
    conn.close()
    print("数据添加成功！")
        

if __name__ == "__main__":
    main()
