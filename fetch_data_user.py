'''
教程 https://www.jianshu.com/p/00f3d1bfa853 
爬取个人微博信息  
'''


from selenium import webdriver
import time
import re
# 全局变量
# 因为用的是chrome 数据，需要下载一个chromedriver.exe
driver = webdriver.Chrome()

def loginWeibo(username, password):
    driver.get('https://passport.weibo.cn/signin/login')
    time.sleep(1)

    driver.find_element_by_id("loginName").send_keys(username)
    driver.find_element_by_id("loginPassword").send_keys(password)

    time.sleep(1)
    driver.find_element_by_id("loginAction").click()

    #driver.close()
  
def visitUserPage(userId):
    driver.get('http://weibo.cn/' + userId)

    print('********************')  
    print('用户资料')
    
    # 1.用户id
    print('用户id:' + userId)
    
    # 2.用户昵称
    strName = driver.find_element_by_xpath("//div[@class='ut']")
    strlist = strName.text.split(' ')
    print("//div[@class='ut']  %s" % strName.text)
    nickname = strlist[0]
    print('昵称:' + nickname)
    
    # 3.微博数、粉丝数、关注数
    strCnt = driver.find_element_by_xpath("//div[@class='tip2']")
    print("//div[@class='tip2']  %s" % strCnt.text)
    pattern = r"\d+\.?\d*" # 匹配数字，包含整数和小数
    cntArr = re.findall(pattern, strCnt.text)
    print(strCnt.text)
    print("微博数：" + str(cntArr[0]))
    print("关注数：" + str(cntArr[1]))
    print("粉丝数：" + str(cntArr[2]))
    
    print('\n********************')
    # 4.将用户信息写到文件里
    with open("weibo.txt", "w", encoding = "gb18030") as file:
        file.write("用户ID：" + userId + '\r\n')
        file.write("昵称：" + nickname + '\r\n')
        file.write("微博数：" + str(cntArr[0]) + '\r\n')
        file.write("关注数：" + str(cntArr[1]) + '\r\n')
        file.write("粉丝数：" + str(cntArr[2]) + '\r\n')
      
    # 5.获取微博内容
    # http://weibo.cn/ + userId + ? filter=0&page=1
    # filter为0表示全部，为1表示原创
    print("微博内容")
    
    pageList = driver.find_element_by_xpath("//div[@class='pa']")
    print(pageList.text)
    pattern = r"\d+\d*"     # 匹配数字，只包含整数
    pageArr = re.findall(pattern, pageList.text)
    totalPages = pageArr[1]   # 总共有多少页微博
    print('总页数',totalPages)
    
    pageNum = 1     # 第几页
    numInCurPage = 1      # 当前页的第几条微博内容
    contentPath = "//div[@class='c'][{0}]"
  
    #while(pageNum <= int(totalPages)):
    while(pageNum <= 3):  
      contentUrl = "http://weibo.cn/" + userId + "?filter=0&page=" + str(pageNum)
      driver.get(contentUrl)
      content = driver.find_element_by_xpath(contentPath.format(numInCurPage)).text
      # print("\n" + content) # 微博内容，包含原创和转发
      if "设置:皮肤.图片.条数.隐私" not in content:
        numInCurPage += 1
        with open("weibo.txt", "a", encoding = "gb18030") as file:
          file.write("\r\n" + "\r\n" + content)  # 将微博内容逐条写到weibo.txt中
      else:
        pageNum += 1            # 抓取新一页的内容
        numInCurPage = 1          # 每一页都是从第1条开始抓    
    
if __name__ == '__main__':
    username = 'tangrongboy@126.com'  # 输入微博账号
    password = 'tang8242+7..'         # 输入密码
    loginWeibo(username, password)   # 要先登录，否则抓取不了微博内容
    
    time.sleep(20)
    uid = 'huangxiaoming'   #黄晓明微博
    visitUserPage(uid)
