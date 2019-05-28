import urllib.request
import requests
from bs4 import BeautifulSoup

f = open("C:/test/channel.txt", 'r')#channel url을 모은 text파일
while True:
    line = f.readline()#한 줄씩 (=한채널씩)읽어와서
    if not line : break
    print(line)
    req = urllib.request
    d = req.urlopen(line)
    stat = d.getheaders()
    if d.status is 200:#채널이 활성화 상태면 
        print("Connect Success")
        print("Get Comment Information")
        req = requests.get(line)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
    else:
        print("Fail")
        print("Get Next Channel")



f.close()
