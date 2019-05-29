import urllib.request
import requests
from bs4 import BeautifulSoup, Tag
from selenium import webdriver
import pytube
f = open("test/channel.txt", 'r')#channel url을 모은 text파일
number=0
while True:
    line = f.readline()#한 줄씩 (=한채널씩)읽어와서
    if not line:
        break
    req = urllib.request
    d = req.urlopen(line)
    stat = d.getheaders()
    if d.status is 200:#채널이 활성화 상태면
        print("Connect Success")
        print("Get Comment Information")
        req = requests.get(line)#채널 진입
        #print(line)
        html = req.content.decode('utf-8', 'replace')
        soup = BeautifulSoup(html, "html.parser")
        k = soup.find_all("h1", "branded-page-header-title")
        name = ""
        for i in k:
            name = i.text.strip().replace('\n', ' ').replace(',', '')
            print(name)
        st = "/videos"
        search_line = line.rstrip('\n')#개행문자 제거
        search_line += st
        print(search_line)
        driver = webdriver.Chrome()
        driver.get(search_line)
        req2 = requests.get(search_line)
        html2 = req2.content.decode('utf8', 'replace')
        soup2 = BeautifulSoup(html2, "html.parser")
        finders = soup2.findAll("h3", {"class": "yt-lockup-title"})
        num = 1
        for finder in finders:
            finder = str(finder)
            #print(finder)
            addr = finder.partition('href="/')[2]
            addr = addr.split('"')[0]
          #  print(addr)
            goal = "https://www.youtube.com/"+addr
            driver.get(goal)
            req3 = requests.get(goal)
            html3 = req3.content.decode('utf-8','replace')
            soup3 = BeautifulSoup(html3, "lxml")
            output = 'test/'+str(number)+"_"+str(num)+'.txt'
            file = open(output, 'w',encoding='utf8') # 내부 구조를 보기 위한것. encoding 작업을 하지 않으면 오류나니까 유의
            file.write(str(soup3))
            file.close()
            num += 1

        driver.close()
    else:
        print("Fail")
        print("Get Next Channel")
    number+=1


f.close()
