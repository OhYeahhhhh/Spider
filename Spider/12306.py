import requests
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from PIL import Image
import os
from io import BytesIO
import urllib.request
import re
from selenium.webdriver.common.action_chains import ActionChains

driver=webdriver.Firefox()
driver.maximize_window()

def getImgCode():
    headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 6.0 x64; en-US; rv:1.9pre)Gecko/2008072421 Minefield/3.0.2pre"}
    imgName="imgCode.jpg"
    src1 = driver.find_element_by_class_name("imgCode").get_attribute("src")
    req = urllib.request.Request(src1, headers=headers)
    resp = urllib.request.urlopen(req, timeout=100)
    data = resp.read()
    if os.path.isfile(imgName):
        os.remove(imgName)
    fobj = open(imgName, "wb")
    fobj.write(data)
    fobj.close()

#验证码解析
def parse_img():
    url="http://littlebigluo.qicp.net:47720/"
    response=requests.request("POST",url,data={"type":"1"},files={'pic_xxfile':open('imgCode.jpg','rb')})
    result=[]
    for i in re.findall("<B>(.*)</B>",response.text)[0].split(" "):
        result.append(int(i)-1)
    return result

#实现验证码自动点击
def move():
    result = parse_img()
    try:
        Action=ActionChains(driver)
        imgCode=driver.find_element_by_class_name("imgCode")
        coordinate=[[-105,-20],[-35,-20],[40,-20],[110,-20],[-105,50],[-35,50],[40,50],[110,50]]
        for i in result:
            Action.move_to_element(imgCode).move_by_offset(coordinate[i][0],coordinate[i][1]).click()
        Action.perform()
    except Exception as e:
        print(e)

def login(userName,password):
    try:
        driver.get('https://kyfw.12306.cn/otn/resources/login.html')
        time.sleep(3)
        account=driver.find_element_by_class_name("login-hd-account")
        account.click()
        username=driver.find_element_by_id('J-userName')
        username.send_keys(userName)
        driver.find_element_by_id("J-password").send_keys(password,Keys.ENTER)
        time.sleep(3)
        getImgCode()
        move()
        driver.find_element_by_class_name('login-btn').click()
        time.sleep(3)
    except:
        print("error")

if __name__ == "__main__": 
    login("18457657675","wss435314080")