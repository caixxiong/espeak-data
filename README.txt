都是在win10下进行的，linux/mac参考教程，或自查，流程差不多

1.python 抓取某条微博下面的评论
需要配置一下环境，安装selenium，下载对应版本的ChromeDriver   
教程：https://www.jianshu.com/p/00f3d1bfa853 ,里面还有一些处理微博内容的代码
fetch_data_usr.py    python爬取微博用户的微博信息

fetch_data_weibo.py    python爬虫新浪微博评论、评论人信息
教程：https://blog.csdn.net/kr2563/article/details/84579504


2.R语言抓取某用户的微博情况，@可视化，代码示例：https://blog.csdn.net/kmd8d5r/article/details/79192006
需要配置环境，教程：https://blog.csdn.net/weixin_40628687/article/details/78971934
                      2.1 在Rstudio中下载RSelenium包和Rwebdriver包：RSelenium包直接install     Rwebdriver包如果按照他的办法下载不了可以百度一下即可。
                      2.2 配置java环境，教程：https://www.cnblogs.com/renqiqiang/p/6822143.html。。我安装的是jdk-8u211-windows-x64.exe。
                      2.3 selenium以及浏览器驱动的下载  （注意对应浏览器版本，没有的需要自查）

在运行R程序进行抓取微博前，需要打开selenium-server和浏览器驱动
先在win10中的cmd运行：
java -Dwebdriver.chrome.driver="D:\java\chromedriver.exe" -jar D:\java\selenium-server-standalone-3.8.1.jar
再去Rstudio中运行程序at_network.R，就可以画图了，还需要改一下。


