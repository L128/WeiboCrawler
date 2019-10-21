from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

# safeUrlopen

# def getSource(url):
#     try:
#         html = urlopen(url)
#     except HTTPError as e:
#         print (e)
#         return None
#     try:
#         bsObj = BeautifulSoup(html.read(), "html.parser")
#     except AttributeError as e:
#         print (e)
#         return None
#     return bsObj

# page = getSource("http://www.pythonscraping.com/pages/warandpeace.html")

# findNamesInGreen

html1 = urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html1, "html.parser")
# namelist = bsObj.findAll("span", {"class":"green"})
for name in bsObj.find("table", {"id":"giftList"}).tr:
    print (name)

