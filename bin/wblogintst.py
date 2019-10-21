#coding=utf-8
import re
import time
import string
import os
import pickle
import requests
from lxml import etree
import traceback
import sys
from bs4 import BeautifulSoup


class weibo:
    cookie = {"Cookie": "_T_WM=18016389465; SUB=_2A25wqBf2DeRhGeFO7lES8inIzT-IHXVQUrm-rDV6PUJbktANLUTMkW1NQXYHGYcIJvbc_OttcydxLd_AJ9gwyeJe; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWJQU0DxL.Q89vQPeF-mTfw5JpX5KzhUgL.FoM7SKe0eoMXSoe2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMNeh-0e0zNShq0; SUHB=05i6UNuzs99dcq; MLOGIN=0; XSRF-TOKEN=6bf020; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000174; WEIBOCN_FROM=1110106030; SSOLoginState=1571579814"} #将your cookie替换成自己的cookie
    header={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'}#这里就是浏览器的头部信息
    def __init__(self,user_id,filter = 0):
        self.user_id = user_id #用户id，即需要我们输入的数字，如昵称为“Dear-迪丽热巴”的id为1669879400
        self.filter = filter #取值范围为0、1，程序默认值为0，代表要爬取用户的全部微博，1代表只爬取用户的原创微博
        self.userName = '' #用户名，如“Dear-迪丽热巴”
        self.weiboNum = 0 #用户全部微博数
        self.weiboNum2 = 0 #爬取到的微博数
        self.following = 0 #用户关注数
        self.followers = 0 #用户粉丝数
        self.location = '' #用户所在地
        self.sex = '' #用户性别
        # self.weibos = [] #微博内容
        # self.num_zan = [] #微博对应的点赞数
        # self.num_forwarding = [] #微博对应的转发数
        # self.num_comment = [] #微博对应的评论数
        # self.weibo_detail_urls=[]#pickle.load(open("weibourl1.pkl", "r"))#微博评论
        # self.weibourls=[]#pickle.load(open('weibourl2.pkl','r'))#每一条微博链接，用于断点续爬

    def getUserName(self):
        try:
            url = 'http://weibo.cn/%d/info'%(self.user_id)
            html = requests.get(url, cookies = weibo.cookie,headers=weibo.header).content  #这一句里面的cookies与headers就实现了登录
            selector = etree.HTML(html)
            userName = selector.xpath("//title/text()")[0]
            self.userName = userName[:-3]
            print ('用户昵称：' + self.userName)
        except Exception as e:
            print (e)

    def getUserInfo(self):
        try:
            url = 'http://weibo.cn/u/%d?filter=%d&page=1' % (self.user_id, self.filter)
            html = requests.get(url, cookies=weibo.cookie, headers=weibo.header).content
            selector = etree.HTML(html)
            pattern = r"\d+\.?\d*"
            str_wb = selector.xpath("//div[@class='tip2']/span[@class='tc']/text()")
            guid = re.findall(pattern, str_wb[0], re.S | re.M)
            for value in guid:
                num_wb = int(value)
                break
            self.weiboNum = num_wb
            print('微博数: ' + str(self.weiboNum))
            str_gz = selector.xpath("//div[@class='tip2']/a/text()")[0]
            guid = re.findall(pattern, str_gz, re.M)
            self.following = int(guid[0])
            print('关注数: ' + str(self.following))

            str_fs = selector.xpath("//div[@class='tip2']/a/text()")[1]
            guid = re.findall(pattern, str_fs, re.M)
            self.followers = int(guid[0])
            print('粉丝数: ' + str(self.followers))

            bsObj = BeautifulSoup(html, "lxml")
            lcsx = bsObj.find(text=re.compile(r'[男女]/[\u4E00-\u9FA5]+'))
            strtmp = ""
            strtmp = strtmp.join(lcsx)
            lcsx2 = str(re.findall(r'[男女]/[\u4E00-\u9FA5]+', strtmp)[0])
            self.location = lcsx2[2:]
            print('用户地区：' + self.location)
            self.sex = lcsx2[0]
            print('用户性别：' + self.sex)

        except Exception as e:
            print(e)

    def getUserFans(self):
        try:
            url = 'http://weibo.cn/%d/fans' % self.user_id
            html = requests.get(url, cookies=weibo.cookie, headers=weibo.header).content
            bsObj = BeautifulSoup(html, "html.parser")
            namelist = bsObj.findAll("a", {"href":re.compile(r"https://weibo.cn/...[0-9]+")},text=True)
            for fan in namelist:
                if re.match(r"https://weibo.cn/u/.[0-9]+", fan["href"]):
                    weibo(int(fan["href"][-10:]), 0).start()
                    # print(fan["href"][-10:])
                else:
                    print(fan["href"][-12:] + " 这个傻逼名字中有CS！")

        except Exception as e:
            print(e)


    def getWeiboInfo(self):
        try:
            url = 'http://weibo.cn/u/%d?filter=%d&page=1' % (self.user_id, self.filter)
            html = requests.get(url, cookies=weibo.cookie, headers=weibo.header).content
            selector = etree.HTML(html)
            if selector.xpath('//input[@name="mp"]') == []:
                pageNum = 1
            else:
                pageNum = int(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
            pattern = r"\d+\.?\d*"
            f = open("./accounts/%s.txt" % self.user_id, "wb")
            for page in range(1, pageNum + 1):
                if page % 10 == 0:
                    print('[ATTEMPTING] rest for 5 minutes to cheat weibo site, avoid being banned.')
                    time.sleep(60 * 5)
                url2 = 'http://weibo.cn/u/%d?filter=%d&page=%d' % (self.user_id, self.filter, page)
                html2 = requests.get(url2, cookies=weibo.cookie, headers=weibo.header).content
                selector2 = etree.HTML(html2)
                info = selector2.xpath("//div[@class='c']")
                if len(info) > 3:
                    for i in range(0, len(info) - 2):
                        detail = info[i].xpath("@id")[0]
                        url3 = 'http://weibo.cn/comment/{}?uid={}&rl=0'.format(detail.split('_')[-1], self.user_id)
                        if url3 not in self.weibo_detail_urls:
                            self.weiboNum2 = self.weiboNum2 + 1
                            # print self.weibo_detail_urls
                            str_t = info[i].xpath("div/span[@class='ctt']")
                            weibos = str_t[0].xpath('string(.)')
                            self.weibos.append(weibos)
                            # print '微博内容：'+ weibos+'***'+'No.%s'%self.weiboNum2
                            str_zan = info[i].xpath("div/a/text()")[-4]
                            guid = re.findall(pattern, str_zan, re.M)
                            num_zan = int(guid[0])
                            self.num_zan.append(num_zan)
                            # print '点赞数: ' + str(num_zan)
                            forwarding = info[i].xpath("div/a/text()")[-3]
                            guid = re.findall(pattern, forwarding, re.M)
                            num_forwarding = int(guid[0])
                            self.num_forwarding.append(num_forwarding)
                            # print '转发数: ' + str(num_forwarding)
                            comment = info[i].xpath("div/a/text()")[-2]
                            guid = re.findall(pattern, comment, re.M)
                            num_comment = int(guid[0])
                            self.num_comment.append(num_comment)
                            # print '评论数: ' + str(num_comment)
                            self.weibo_detail_urls.append(url3)
                            text = str(self.weiboNum2) + ':' + weibos + '\t' + '点赞数：' + str(
                                num_zan) + '\t' + ' 转发数：' + str(num_forwarding) + '\t' + ' 评论数：' + str(
                                num_comment) + '\n'
                            f.write(text.encode())
                            pickle.dump(self.weibo_detail_urls, open("weibourl1.pkl", "wb"))
                        else:
                            print(url3 + '这条微博已经爬取过，忽略')
            if self.filter == 0:
                print('共' + str(self.weiboNum2) + '条微博')
            else:
                print('共' + str(self.weiboNum) + '条微博，其中' + str(self.weiboNum2) + '条为原创微博')
        except Exceptione as e:
                print(e)

    def get_weibo_detail_comment(self):
        weibo_comments_save_path = './weibo/{}.txt'.format(self.user_id)
        with open(weibo_comments_save_path, 'a') as f:
            for i, url in enumerate(self.weibo_detail_urls):
                if url not in self.weibourls:
                    self.weibourls.append(url)
                    pickle.dump(self.weibourls, open("weibourl2.pkl", "w"))
                    print('solving weibo detail from {}'.format(url))
                    html_detail = requests.get(url, cookies=weibo.cookie, headers=weibo.header).content
                    selector = etree.HTML(html_detail)
                    str1 = 'id="pagelist"'
                    if str1 in html_detail:
                        all_comment_pages = selector.xpath('//*[@id="pagelist"]/form/div/input[1]/@value')[0]
                    else:
                        all_comment_pages = 1
                    print('\n这是 {} 的微博：'.format(self.userName))
                    # print('微博内容： {}'.format(self.weibos[i]))
                    # print('接下来是下面的评论：\n\n')
                    f.writelines('微博内容： {}'.format(self.weibos[i]) + '\n')
                    f.writelines('接下来是下面的评论:\n')
                    for page in range(1, int(all_comment_pages) + 1):
                        if page % 10 == 0:
                            print('[ATTEMPTING] rest for 5 minutes to cheat weibo site, avoid being banned.')
                            time.sleep(60 * 5)
                        detail_comment_url = url + '&page=' + str(page)
                        try:
                            html_detail_page = requests.get(detail_comment_url, cookies=weibo.cookie,
                                                            headers=weibo.header).content
                            selector = etree.HTML(html_detail_page)
                            comment_div_element = selector.xpath('//div[starts-with(@id, "C_")]')
                            for child in comment_div_element:
                                single_comment_user_name = child.xpath('a[1]/text()')[0]
                                if child.xpath('span[1][count(*)=0]'):
                                    single_comment_content = child.xpath('span[1][count(*)=0]/text()')[0]
                                else:
                                    span_element = child.xpath('span[1]')[0]
                                    at_user_name = span_element.xpath('a/text()')[0]
                                    at_user_name = '$' + at_user_name.split('@')[-1] + '$'
                                    single_comment_content = span_element.xpath('/text()')
                                    single_comment_content.insert(1, at_user_name)
                                    single_comment_content = ' '.join(single_comment_content)
                                full_single_comment = '<' + single_comment_user_name + '>' + ': ' + single_comment_content
                                # print(full_single_comment)
                                f.writelines(full_single_comment + '\n')
                        # f.writelines('F\n')
                        except etree.XMLSyntaxError as e:
                            print('user id {} all done!'.format(self.user_id))
                            print('all weibo content and comments saved into {}'.format(weibo_comments_save_path))
                    f.writelines('F\n')
                else:
                    print('has already')

    def writeTxt(self):
        try:
            # if self.filter == 1:
            #     resultHeader = '\n\n原创微博内容：\n'
            # else:
            #     resultHeader = '\n\n微博内容：\n'
            result = \
                '用户信息\n用户昵称：' + self.userName + \
                '\n用户id：' + str(self.user_id) + \
                '\n微博数：' + str(self.weiboNum) + \
                '\n关注数：' + str(self.following) + \
                '\n粉丝数：' + str(self.followers) + \
                '\n所在地：' + self.location + \
                '\n性别：' + self.sex
                # + resultHeader
            # if os.path.isdir('weibo') == False:
            #     os.mkdir('weibo')
            f = open("./accounts/%s.txt" % self.user_id, "wb")
            f.write(result.encode())
            f.close()
        except Exception as e:
            print(e)

    def start(self):
        try:
            weibo.getUserName(self)
            weibo.getUserInfo(self)
            weibo.writeTxt(self)
            # weibo.getWeiboInfo(self)
            # weibo.get_weibo_detail_comment(self)
            print
            '信息抓取完毕'
            print
            '==========================================================================='
        except Exception as e:
            print(e)


user_id = 6924853690  # 可以改成任意合法的用户id（爬虫的微博id除外）
filterr = 0  # 值为0表示爬取全部的微博信息（原创微博+转发微博），值为1表示只爬取原创微博
# open('./weibourl1.pkl','w')
# open('./weibourl2.pkl','w')
# wb.start()  # 爬取微博信息
# print('用户名：' + wb.userName)
# print('全部微博数：' + str(wb.weiboNum))
# print('关注数：' + str(wb.following))
# print('粉丝数：' + str(wb.followers))
# print('最新一条微博为：' + wb.weibos[0])  # 若filter=1则为最新的原创微博，如果该用户微博数为0，即len(wb.weibos)==0,打印会出错，下同
# print('最新一条微博获得的点赞数：' + str(wb.num_zan[0]))
# print('最新一条微博获得的转发数：' + str(wb.num_forwarding[0]))
# print('最新一条微博获得的评论数：' + str(wb.num_comment[0]))

wb = weibo(user_id, filterr)  # 调用weibo类，创建微博实例wb
wb.getUserFans()
