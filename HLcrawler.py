#headless chrome 으로 crawler를 만들려고 시도
#실질적으로 성공은 했으나 품질이 기존 chrome에 비해 한참 떨어짐
#따라서 기존 chrome으로 제작하되 결과물을 mysql과 연동할 수 있도록 파일의 DB화를 준비 중

import urllib.request
from urllib.request import urlopen
import requests
from bs4 import BeautifulSoup, Tag
import os
from selenium import webdriver
import re
from selenium.webdriver.common.keys import Keys
import time

options = webdriver.ChromeOptions()
options.add_argument('--disable-extensions')
options.add_argument('--headless')
options.add_argument('window-size=1920x1080')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('chromedriver', chrome_options=options)


f = open('test/channel.txt', 'r')
yid = 0
while True:
    line = f.readline()
    if not line:
        break;
    req = urllib.request
    d = req.urlopen(line)
    stat = d.getheaders()
    if d.status is 200:
        print("Connect Success")
        print("Get Information")
        print(line)
        page_info = urlopen(line)
        soup = BeautifulSoup(page_info, 'html.parser')
        ynames=soup.head.find_all('meta')
        yname = ynames[0].get('content')
        print(yname)
        yInfo = 'yInfo/'
        if not os.path.isdir(yInfo):
            os.mkdir(yInfo)
        #Search Youtuber's name
        output_path = 'articles/'
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        output_path += str(yname)
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        #Make Folders
        line = line.rstrip('\n')
        st = '/videos'
        line += st
        print(line)

        driver.get(line)
        driver.implicitly_wait(3)
        req2 = requests.get(line)
        html2 = req2.content.decode('utf8', 'replace')
        soup2 = BeautifulSoup(html2, "html.parser")
        finders = soup2.findAll("h3", {"class": "yt-lockup-title"})
        ano = 0
        for finder in finders:
            finder = str(finder)
            addr = finder.partition('href="/')[2]
            addr = addr.split('"')[0]
            goal = "https://www.youtube.com/"+addr
            print(goal)
            video_info = urlopen(goal)
            soup3 = BeautifulSoup(video_info, 'html.parser')
            titles = soup3.head.find_all('meta')

            driver.get(goal)
            driver.implicitly_wait(3)
            page_down_cnt = 20
            start_scroll = 0
            while page_down_cnt:
                driver.find_element_by_tag_name('body').send_keys(Keys.END)
                page_down_cnt -= 1
                time.sleep(0.3)
            output_file = output_path+'/'+str(ano)+'.txt'
            f2 = open(output_file, 'w', encoding='utf8')
            con = str(titles[0].get('content'))
            content = re.sub(' [^0-9a-zA-Zㄱ-힗]()-', '', con)
            print(content)
            f2.write(str(yid)+'\n')
            f2.write(str(ano)+'\n')
            f2.write(content+'\n')
            f2.write(goal+'\n')
            f2.close()
            ano += 1
 #           html3 = driver.page_source
 #           soup3 = BeautifulSoup(html3, "html.parser")
 #           commentaddrs = soup3.findAll("yt-formatted-string",
 #                                        {"class": "style-scope ytd-comment-renderer", "id": "content-text",
 #                                         "slot": "content"})
  #          output = 'comments/' + str(number)
   #         if not os.path.isdir(output):
    #            os.mkdir(output)
     #       output += "/" + str(num) + '.txt'
      #      file = open(output, 'w', encoding='utf8')  # 내부 구조를 보기 위한것. encoding 작업을 하지 않으면 오류나니까 유의
       #     for commentaddr in commentaddrs:
#                commentaddr = str(commentaddr)
 #               comment = commentaddr.partition('split-lines="">')[2]
  #              comment = comment.partition('</yt-formatted-string')[0]
  #              comment += '\n'
   #             file.write(comment)
  #          file.close()
   #         num += 1
    yid += 1
f.close()
driver.quit()

