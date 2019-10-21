import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.keys import Keys


chromePath = r'/Users/louhaotian/Documents/Weibo/venv/bin/chromedriver'
wd = webdriver.Chrome(executable_path= chromePath) #构建浏览器
loginUrl = 'https://passport.weibo.cn/signin/login?'
# loginUrl = 'https://cn.bing.com'
wd.get(loginUrl) #进入登陆界面
wd.maximize_window()
# wd.find_element_by_id("sb_form_q").send_keys("ss")
wd.find_element_by_xpath('//*[@id="loginWrapper"]/form/section/div[1]/p').send_keys('18822818747') #输入用户名
# wd.find_element_by_xpath('//*[@id="loginPassword"]').send_keys('Aptx4869') #输入密码
# wd.find_element_by_xpath('//*[@id="loginAction"]').click() #点击登陆
# req = requests.Session() #构建Session
# cookies = wd.get_cookies() #导出cookie
# for cookie in cookies:
#     req.cookies.set(cookie['name'],cookie['value']) #转换cookies
# test = req.get('https://weibo.cn')