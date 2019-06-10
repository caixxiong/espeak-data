# -*- coding:utf-8 -*- 
'''
教程：https://blog.csdn.net/kr2563/article/details/84579504
爬取某条微博下面的评论信息
'''
import requests
import xlwt
import  re
import json
import time 

#工具类，用来去除爬取的正文中一些不需要的链接、标签等
class Tool:
    '''还可以研究一下，去掉表情等
    '''
    deleteImg = re.compile('<img.*?>')
    newLine =re.compile('<tr>|<div>|</tr>|</div>')
    deleteAite = re.compile('//.*?:')
    deleteAddr = re.compile('<a.*?>.*?</a>|<a href='+'\'https:')
    deleteTag = re.compile('<.*?>')
    deleteWord = re.compile('回复@|回覆@|回覆|回复')
 
    @classmethod
    def replace(cls,x):
        x = re.sub(cls.deleteWord,'',x)
        x = re.sub(cls.deleteImg,'',x)
        x = re.sub(cls.deleteAite,'',x)
        x = re.sub(cls.deleteAddr, '', x)
        x = re.sub(cls.newLine,'',x)
        x = re.sub(cls.deleteTag,'',x)
        return x.strip()
 
# 获取评论 
def get_comment(headers, weibo_id='H1rMeFWa2',max_page=10,max_comment=100):
    '''
    headers:cookie信息
    weibo_id：需要爬取的某条微博的id
    max_page：评论页数
    max_comment：最大评论数
    timesleep：每一页的休眠时间
    '''
    
    count = 0
    i = 0
    File = open('filename','w',encoding='utf-8')
    excel = xlwt.Workbook(encoding='utf-8')
    sheet = excel.add_sheet('sheet1')
    sheet.write(0,0,'id')
    sheet.write(0,1,'sex')
    sheet.write(0,2,'name')
    sheet.write(0,3,'time')
    sheet.write(0,4,'loc')
    sheet.write(0,5,'text')
    sheet.write(0,6,'likes')
    
    # 抓取微博条数&页数（手机端）
    while count < max_comment and i < max_page:
        i += 1 
        # 教程https://blog.csdn.net/kr2563/article/details/84579504
        #url = 'https://m.weibo.cn/api/comments/show?id=H1rMeFWa2&page='+str(i) # 更新url
        url = 'https://m.weibo.cn/api/comments/show?id={}&page={}'.format(weibo_id,i)
        print (url)
        try:
            response = requests.get(url,headers=headers) 
            print(response)
            resjson = json.loads(response.text) 
            print(resjson)
            data = resjson.get('data')
            datanext = data.get('data')  #还有其他信息可以爬取
            for j in range(0,len(datanext)):
                count += 1
                temp = datanext[j]
                text = temp.get('text')
                text = Tool.replace(text)
                File.write(str(text) + "\n")
                like_counts = temp.get('like_counts')
                created_at = temp.get('created_at')
                user = temp.get('user')
                screen_name = user.get('screen_name')
                userid = user.get('id')
                info_url = "https://m.weibo.cn/api/container/getIndex?containerid=230283"+str(userid)+"_-_INFO" # 转发人信息的url
                r = requests.get(info_url)
                infojson = json.loads(r.text)
                infodata = infojson.get('data')
                cards = infodata.get('cards')
                sex = ''
                loc = ''
                for l in range(0,len(cards)):
                    temp = cards[l]
                    card_group = temp.get('card_group')
                    for m in range(0,len(card_group)):
                        s = card_group[m]
                        if s.get('item_name') == '性别':
                            sex = s.get('item_content')
                        if s.get('item_name') == '所在地':
                            loc = s.get('item_content')
                if sex is None:
                    sex = '未知'
                if loc is None:
                    loc = '未知'
                sheet.write(count,0,userid)
                sheet.write(count,1,str(sex))
                sheet.write(count,2,str(screen_name))
                sheet.write(count,3,created_at)
                sheet.write(count,4,text)
                sheet.write(count,5,str(loc))
                sheet.write(count,6,like_counts)
            print ("已经抓取"+str(count)+"条数据")
            time.sleep(20)# 延时20s才不会被封
        except Exception as e:
            print (e)
    excel.save('filename.xls')
    return response
 
 
if __name__ == '__main__':
    
    # cookie获取教程：https://blog.csdn.net/qq_41057280/article/details/81304099 
    # 先仔网页上登陆自己的微博
    headers = {
        'User-agent' : 'Mozilla/5.0',
        'Cookie':'_s_tentry=passport.weibo.com; Apache=4644725909837.164.1537707872923; SINAGLOBAL=4644725909837.164.1537707872923; ULV=1537707872999:1:1:1:4644725909837.164.1537707872923:; YF-Ugrow-G0=169004153682ef91866609488943c77f; YF-V5-G0=a5a6106293f9aeef5e34a2e71f04fae4; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFORXWccqc7gPqZ6oQpoKWA5JpX5oz75NHD95QESo.7SK5ReKM0Ws4Dqcjdi--fiK.XiK.7i--fiK.fiKyWi--Ri-zpi-z4; ALF=1561973602; SUB=_2A25x9jYyDeRhGeRI4lIU8CbNzD-IHXVTGVp6rDV8PUJbkNBeLWqikW1NUpNw9jP7rdotmqdVd-M30oUGPA61hMk8; wvr=6; YF-Page-G0=536a03a0e34e2b3b4ccd2da6946dab22|1559381837|1559381837; UOR=,,www.baidu.com; wb_view_log_2690508173=1920*10801%261600*9001; webim_unReadCount=%7B%22time%22%3A1559442050786%2C%22dm_pub_total%22%3A5%2C%22chat_group_pc%22%3A0%2C%22allcountNum%22%3A5%2C%22msgbox%22%3A0%7D'
    }
     
    # 获取微博id教程：https://blog.csdn.net/kr2563/article/details/84579504
    resjson = get_comment(headers=headers,weibo_id='H1rMeFWa2',max_page=10,max_comment=100) 


'''还有其他信息可以爬取,有挺多东西的，可以从resjson查看一下
'''

