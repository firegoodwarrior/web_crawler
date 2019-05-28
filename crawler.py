import urllib.request
import requests
from bs4 import BeautifulSoup, Tag
from selenium import webdriver

f = open("test/channel.txt", 'r')#channel url을 모은 text파일
while True:
    line = f.readline()#한 줄씩 (=한채널씩)읽어와서
    if not line : break
    req = urllib.request
    d = req.urlopen(line)
    stat = d.getheaders()
    if d.status is 200:#채널이 활성화 상태면
        print("Connect Success")
        print("Get Comment Information")
        req = requests.get(line)
        #print(line)
        html = req.content.decode('utf-8', 'replace')
        soup = BeautifulSoup(html, "html.parser")
        k = soup.find_all("h1", "branded-page-header-title")
        for i in k:
            name = i.text.strip().replace('\n', ' ').replace(',', '')
            print(name)
        st = "/videos"
        search_line = line.rstrip('\n')#개행문자 제거
        search_line += st
        print(search_line)
        driver = webdriver.Chrome()
        driver.get(search_line)


    else:
        print("Fail")
        print("Get Next Channel")



f.close()
