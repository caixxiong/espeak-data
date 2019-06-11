import os
import re
import time
from selenium import webdriver

driver = webdriver.Chrome()


# 登录
def login_weibo(name, passwd):
    driver.get('https://passport.weibo.cn/signin/login')
    time.sleep(1)
    driver.find_element_by_id("loginName").send_keys(name)
    driver.find_element_by_id("loginPassword").send_keys(passwd)
    time.sleep(1)
    driver.find_element_by_id("loginAction").click()


# 访问主页
def visit_main_page(user_url):
    driver.get(user_url)

    # 用户字符串类信息
    str_infos = driver.find_element_by_xpath("//div[@class='ut']").text
    nick_name, sex_area, _, identify, signature = str_infos.strip().split()[: 5]

    # 用户数字类信息
    num_infos = driver.find_element_by_xpath("//div[@class='tip2']").text
    pattern = r"\d+\.?\d*"  # 匹配数字，包含整数和小数
    weibo_num, follow_num, fans_num = re.findall(pattern, num_infos)[: 3]
    uid = user_url.split("/")[-1]

    # 用户头像
    head_pic_url = driver.find_element_by_xpath("//a/img[@alt='头像']").get_attribute("src")
    head_pic_save_name = head_pic_url, "/home/caixiong/AVisual/weibo/head_pitcures/" + uid + "." + head_pic_url.split(".")[-1]
    os.system("wget '%s' -o '%s'" % (head_pic_url, head_pic_save_name))
    base_infos = [uid, weibo_num, follow_num, fans_num, nick_name, sex_area, identify, signature, user_url, head_pic_url]

    print("HHHH")
    # 获取关注和粉丝页面的url
    urls = driver.find_elements_by_xpath("//div[@class='tip2']/a")
    follow_url, fans_url = [x.get_attribute("href") + "?page=" for x in urls[: 2]]
    follows, fanses = [], []
    for url, ans_list in zip([follow_url, fans_url], [follows, fanses]):
        for i in range(1, 21):
            one_page = visit_follow_fans_page(url + str(i))
            ans_list.extend(one_page)
            # print(one_page)
            time.sleep(1.0)
    return base_infos, follows, fanses


def visit_follow_fans_page(url):
    driver.get(url)
    td_list = driver.find_elements_by_xpath("//tr/td")
    follow_fans_urls = []
    for x in td_list:
        if not x.text:
            continue
        nick_name = x.text.strip().split()[0]
        main_page_url = x.find_element_by_link_text(nick_name).get_attribute("href")
        follow_fans_urls.append(main_page_url)
    return follow_fans_urls


def save_datas(idx, ff, base_infos, follows, fanses):
    ff.write(str(idx) + "\n")
    ff.write("**********\n")
    follows = [x.split("/")[-1] for x in follows]
    fanses = [x.split("/")[-1] for x in fanses]
    ff.write("||".join(base_infos) + "\n")
    ff.write("||".join(follows) + "\n")
    ff.write("||".join(fanses) + "\n")
    ff.write("**********")


def main():
    login_name = "tangrongboy@126.com"
    login_passwd = "tang8242+7.."
    url = 'https://weibo.cn/huangxiaoming'

    # 登录自己的微博账户
    login_weibo(login_name, login_passwd)
    time.sleep(5)

    step = 5000
    with open("weibo_users.txt", "a") as ff:
        # 访问主页
        for x in range(step):
            base_infos, follows, fanses = visit_main_page(url)
            save_datas(x, ff, base_infos, follows, fanses)
            url = fanses[0]
            print("!!!!%d!!!!" % x, base_infos[:5])


if __name__ == "__main__":
    main()
