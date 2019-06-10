from selenium import webdriver
import time
import re

driver = webdriver.Chrome()


# 登录
driver.get('https://passport.weibo.cn/signin/login')
time.sleep(1)
driver.find_element_by_id("loginName").send_keys('tangrongboy@126.com')
driver.find_element_by_id("loginPassword").send_keys('tang8242+7..')
time.sleep(10)
driver.find_element_by_id("loginAction").click()
time.sleep(10)

# 访问页面
uid = 'huangxiaoming'
driver.get('http://weibo.cn/' + uid)

print("用户id: " + uid)

str_ut = driver.find_element_by_xpath("//div[@class='ut']")
print("//div[@class='ut']\n******************\n", str_ut.text)
print("*******************\n\n")
str_tip2 = driver.find_element_by_xpath("//div[@class='tip2']")
print("//div[@class='tip2']\n******************\n", str_tip2.text)
print("*******************\n\n")

# 获取粉丝,关注的url
urls = driver.find_elements_by_xpath("//div[@class='tip2']/a")
for url in urls: 
    print(url.get_attribute("href")) 
