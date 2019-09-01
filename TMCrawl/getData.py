# coding=utf-8
import re
import locale
import io
import sys
import time
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urlopen
class crawlTianMao():
    def __init__(self,brand,url):#传入需要统计的品牌，目的URL
        self.__brand__ = brand
        self.__url__ = url
        self.__count__ = 1
        # sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')#解决中文乱码问题
        # sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        # locale.getpreferredencoding()
        # locale.getdefaultlocale()
    def go(self):
        # browserOptions = webdriver.ChromeOptions()                                             #启用浏览器用户选项
        # prefs = {"profile.managed_default_content_settings.images": 2}                         #设置浏览器不加载图片
        # browserOptions.add_experimental_option("prefs", prefs)
        # browserOptions.add_argument("--proxy-server=http://61.143.38.53:8118")
        # browserOptions.headless = True                                                       #设置浏览器无界面化
        browser = webdriver.Chrome(executable_path='chromedriver.exe')#启用谷歌自动测试软件返回浏览器对象
        # browser = webdriver.Firefox(executable_path='geckodriver.exe')                       # 启用火狐自动测试工具返回浏览器对象
        browser.get(self.__url__)                                                              # 访问网站
        return browser

    def getCookies(self):
        url = 'https://www.tmall.com/'
        browser = crawlTianMao.go(self)
        if(self.__url__ == url):
             try:
                  print("-----------------------------------------------------------------------@WEID------------------------------------------------------------------------------")
                  print('1、正在进行登录!')
                  browser.find_element_by_class_name('menu-hd').click()                       #自动化登录网站
                  browser.find_element_by_link_text('密码登录').click()
                  browser.find_element_by_class_name('weibo-login').click()
                  browser.find_element_by_name('username').send_keys('Your Username')
                  browser.find_element_by_name('password').send_keys('Your Password')
                  browser.find_element_by_class_name('W_btn_g ').click()
                  cookies = browser.get_cookies()                                              #获取cookie
                  print('2、获取cookie成功！')
                  try:
                       df = pd.DataFrame(cookies)                                              #存储cookie到本地文件
                       df.to_csv('cookies.csv')
                       print('3、写入cookie成功！')
                  except:
                       print('写入cookie失败！')
                  try:
                      time.sleep(5)                                                            #强制等待时间
                      browser.find_element_by_link_text('淘宝网首页').click()                  #进入淘宝首页
                      browser.current_window_handle
                      print('4、正在进入淘宝首页!')
                      print(browser.title)
                      print('5、进入淘宝首页成功!')
                      time.sleep(5)
                      browser.find_elements_by_link_text("天猫")[0].click()                    #进入天猫首页
                      browser.switch_to.window(browser.window_handles[1])                      #锁定到新的页面
                      print('6、正在进入天猫首页!')
                      browser.current_window_handle                                            #锁定当前页面
                      print(browser.title)
                      time.sleep(5)
                      print('7、进入天猫首页成功！')
                      time.sleep(5)
                      browser.find_element_by_id('mq').send_keys(self.__brand__)              #自动输入文本框
                      browser.find_elements_by_tag_name('button')[0].click()                  #搜索
                      print('8、搜索'+self.__brand__+'成功！')

                  except:
                      print('Error：进入淘宝首页失败!')
                      print('Error：进入天猫首页失败！')
                      print('Error：搜索' + self.__brand__ + '失败！')

                  try:
                      browser.current_window_handle
                      print('9、准备采集数据！')
                      print("-----------------------------------------------------------------------@WEID------------------------------------------------------------------------------")
                      bsobj = crawlTianMao.getHTML(self,browser)
                      # print('asd')
                      crawlTianMao.filterHTML(self,bsobj)
                      print('采集第一页成功！')
                      self.__count__ = self.__count__ + 1
                      print("-----------------------------------------------------------------------@WEID------------------------------------------------------------------------------")
                      pagecount = bsobj.find('form',attrs={'name':'filterPageForm'}).text   #获取指定的标签
                      # print(pagecount)
                      # print(type (pagecount))
                      pagecount = int(re.findall("\d+", pagecount)[0])                         #获取总页数
                      print('总页数：'+str(pagecount))
                      while(self.__count__ < pagecount):                                       #自动化爬取页面
                         try:
                             browser = crawlTianMao.clickNext(self, browser)
                             # if(browser.find_elements_by_tag_name('p')[0].text.strip()=='亲，小二正忙，滑动一下马上回来'):
                             #     print(browser.find_elements_by_tag_name('p')[0].text)
                             # elif(browser.find_elements_by_tag_name('h2')[0].text.strip()=='喵~没找到与“ 华为 ”相关的 商品 哦，要不您换个关键词我帮您再找找看')
                             #     chromeOptions = webdriver.ChromeOptions()
                             #     chromeOptions.add_argument("--proxy-server=http://202.20.16.82:10152")
                             bsobj = crawlTianMao.getHTML(self, browser)
                             crawlTianMao.filterHTML(self, bsobj)
                             self.__count__ = self.__count__ + 1
                             print("-----------------------------------------------------------------------@WEID------------------------------------------------------------------------------")
                             # print(self.__count__)
                         except:
                             continue

                  except:
                      print('Error：采集数据失败！')
             except:
                  print('Error：登录失败，正在重新登录！')
                  crawlTianMao.getCookies(self)
             finally:
                  print('结束')
                  print("-----------------------------------------------------------------------@WEID------------------------------------------------------------------------------")

    def clickNext(self,browser):                                                                #点击跳转
        browser.current_window_handle
        print('即将进入第'+str(self.__count__)+'页')
        time.sleep(5)
        try:
           browser.find_element_by_name('jumpto').clear()
           time.sleep(5)
           browser.find_element_by_name('jumpto').send_keys(str(self.__count__))
           time.sleep(5)
           browser.find_elements_by_class_name('ui-btn-s')[1].click()
           time.sleep(5)
           browser.current_window_handle
           print('进入第' + str(self.__count__) + '页成功')
        except:
           print('进入第' + str(self.__count__) + '页失败')
           print('重新尝试进入第' + str(self.__count__) + '页')
           crawlTianMao.clickNext(self,browser)
        return browser

    def getHTML(self,browser):                                                                  #将网页转化为BeautifulSoup对象
        # browser = crawlTianMao.go(self)
        browser.current_window_handle
        time.sleep(5)
        html = browser.page_source                                                              #获取网页源数据
        bsobj = BeautifulSoup(html,'lxml')
        return bsobj

    def filterHTML(self,bsobj):                                                                 #过滤和规范数据
        product,price,store,sales,middle = np.full(65,None),np.full(65,None),np.full(65,None),np.full(65,None),np.full(65,None)
        middle_2 = []                                                                           #以固定长度定义产品，商店等数组
        print('1、初始化过滤工具......')
        if(self.__brand__ == '华为'):
           self.__brand__ = "Huawei"+"/"+self.__brand__                                        #以网站内容形式规范检索文本
        elif(self.__brand__ == '三星'):
            self.__brand__ = "Samsung"+"/"+self.__brand__
        print('2、初始化完毕......')
        print('3、开始获取产品价格......')

        #产品的价格
        ems = bsobj.find_all('em',attrs={'title':True})
        # print(len(ems))
        for i in range(0,len(ems),1):
           price[i] = (ems[i].text)
        print('4、完成产品价格的获取......')
        print('5、开始获取产品型号......')


        #产品的型号
        a = bsobj.find_all('a',attrs={'title':True})
        for i in range(0,len(a),1):
            if(a[i].text.startswith(self.__brand__) or a[i].text.startswith('Huawei/') or a[i].text.startswith('华为')):
                middle_2.append(a[i].text)
        # print(len(a))
        for j in range(0,len(middle_2),1):
            product[j] = middle_2[j]
        # print(middle)
        print('6、完成产品型号的获取......')
        print('7、开始获取产品的销售渠道......')


        #产品旗舰店
        store_a = bsobj.find_all('a',attrs={'class':'productShop-name'})
        for i in range(0,len(store_a),1):
               store[i] = (store_a[i].text[1:-1])
        print('8、完成产品销售渠道的获取......')
        print('9、开始获取产品的销量......')


        #产品月销售量
        ems_sales = bsobj.find_all('p',attrs={'class':'productStatus'})
        # print(len(ems_sales))
        for i in range(0,len(ems_sales),1):
            sales[i] = (ems_sales[i].find_next().text[6:-1])
        print('10、完成产品销售量的过滤......')
        for k in  range(0,len(ems_sales),1):
           if(sales[k].endswith('万')):
               sales[k] = str(float(sales[k][0:-1])*10000)
        print('11、完成产品销售量的获取......')


        #整理数据
        print('12、开始产品数据的整合......')
        data = pd.DataFrame({'产品': product,
                            '月销量': sales,
                            '价格':price,
                            '店铺':store,
                         })
        print('13、完成产品数据的整合......')

        #存储数据到本地文件
        # data.to_csv('HuaWei'+str(self.__count__)+'.csv')
        print('14、生成'+str(self.__brand__)+str(self.__count__)+'.csv文件成功')
        print("-----------------------------------------------------------------------@WEID------------------------------------------------------------------------------")

def main():
    crawlTM = crawlTianMao(brand="华为",url='https://www.tmall.com/')
    crawlTM.getCookies()

if __name__ == '__main__':
    main()
