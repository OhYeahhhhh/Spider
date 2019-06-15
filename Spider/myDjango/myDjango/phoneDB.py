from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import threading
import datetime
from django.http import HttpResponse
from myApp.models import Phones


headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre)Gecko/2008072421 Minefield/3.0.2pre"}
imagePath = "static\\download"
firefox_option=Options()
firefox_option.add_argument('-headless')
driver=webdriver.Firefox(options=firefox_option)

def startUp(url,key):
    try:
        if not os.path.exists(imagePath):
            os.mkdir(imagePath)
        images = os.listdir(imagePath)
        for img in images:
            s = os.path.join(imagePath, img)
            os.remove(s)
    except Exception as err:
        print(err) 
        
    driver.get(url)
    keyInput=driver.find_element_by_id("key")
    keyInput.send_keys(key)
    keyInput.send_keys(Keys.ENTER) 
        
def closeUp():
    try:
        driver.close()
    except Exception as err:
        print(err)

def download(src1,src2,mFile):
    data=None
    if src1:
        try:
            req = urllib.request.Request(src1, headers=headers)
            resp = urllib.request.urlopen(req, timeout=400)
            data = resp.read()
        except:
            pass
    if not data and src2:
        try:
            req = urllib.request.Request(src2, headers=headers)
            resp = urllib.request.urlopen(req, timeout=400)
            data = resp.read()
        except:
            pass
    if data:
        fobj = open(imagePath + "\\" + mFile, "wb")
        fobj.write(data)
        fobj.close()

threads=[]
No=0
pNo=[]
pBrand=[]
pPrice=[]
pContent=[]
pFile=[]

def processSpider():
    try:
        time.sleep(3)
        print(driver.current_url)
        driver.execute_script("window.scrollBy(0,7000)",'1000')
        time.sleep(5)
        lis = driver.find_elements_by_xpath("//div[@id='J_goodsList']//li[@class='gl-item']")
        for li in lis:
            try:
                src1 = li.find_element_by_xpath(".//div[@class='p-img']//a//img").get_attribute("src")
            except:
                src1=""
            try:
                src2 = li.find_element_by_xpath(".//div[@class='p-img']//a//img").get_attribute("data-lazy-img")
            except:
                src2=""
            try:
                price = li.find_element_by_xpath(".//div[@class='p-price']//i").text
            except:
                price="0"
            pPrice.append(price)

            try:
                content = li.find_element_by_xpath(".//div[@class='p-name p-name-type-2']//em").text
                brand = content.split(" ")[0]
                brand = brand.replace("爱心东东\n", "")
                brand = brand.replace(",", "")
                content = content.replace("爱心东东\n", "")
                content = content.replace(",","")
            except:
                brand=""
                content="" 
            pBrand.append(brand)
            pContent.append(content)

            global No
            No+=1
            no = str(No)
            while len(no) < 6:
                no = "0" + no
            pNo.append(no)

            if src1:
                src1=urllib.request.urljoin(driver.current_url,src1)
                p = src1.rfind(".")
                mFile = no + src1[p:]
            elif src2:
                src2=urllib.request.urljoin(driver.current_url,src2)
                p = src2.rfind(".")
                mFile = no + src2[p:]
            if src1 or src2:
                T=threading.Thread(target=download,args=(src1,src2,mFile))
                T.setDaemon(False)
                T.start()
                threads.append(T)
            else:
                mFile = ""
            pFile.append(mFile)
            print(no,brand,price,mFile)
        try:
            driver.find_element_by_xpath("//span[@class='p-num']//a[@class='pn-prev dosabled']")
        except: 
            nextPage=driver.find_element_by_xpath("//span[@class='p-num']//a[@class='pn-next']")
            nextPage.click()
        processSpider()
    except Exception as err:
        print(err)
        
    return pNo,pBrand,pContent,pPrice,pFile

def insertDB(request):
    starttime = datetime.datetime.now()
    url="http://www.jd.com"
    print("Spider starting......")
    startUp(url,"手机")
    pNo,pBrand,pContent,pPrice,pFile = processSpider()
    closeUp()
    print("Spider completed......")
    endtime = datetime.datetime.now()
    elapsed = (endtime - starttime).seconds
    print("Total ", elapsed, " seconds elapsed")
    for i in range(0,len(pNo)):
        phoneDB=Phones(pNo=pNo[i],pBrand=pBrand[i],pPrice=pPrice[i],pContent=pContent[i],pFile=pFile[i])
        phoneDB.save()
    for t in threads:
        t.join()
    print("Spider completed......")

    return HttpResponse("<p>数据添加成功！</p>")