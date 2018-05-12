# coding:utf-8
import time,random

from bs4 import BeautifulSoup
from selenium import webdriver


from apps.book.models import Book,BookType


# http://search.jd.com/bookadvsearch?keyword=Python&ep1=&ep2=

# 第一步 加载html

# 第二步 解析数据保存

# 第三步 点击下一页 并重复第一步操作?


def crawl(start_url,keyword,maxpage):

    url = start_url % keyword           #拼接Url
    driver = webdriver.PhantomJS()      #创建无界面浏览器对象
    driver.get(url)                     #开始浏览


    page = 0
    i = 0

    while(page <= maxpage):

        page += 1
        driver.implicitly_wait(5)

        while(True):
            try:
                driver.find_element_by_css_selector("div[class='notice-loading-more']")   #判断是否还有未加载的商品(当该div存在时则表示还存在商品未加载)
                time.sleep(0.2)
                print('--------------------------------------------------还未加载完毕--------------------------------------------------')
                driver.execute_script("window.scrollBy(0,600)")    #模仿向下滚动600px
            except:
                #当加载完毕则跳出循环
                driver.execute_script("window.scrollBy(0,5000)")
                print('******************************************!!!!!!!!!加载完毕!!!!!!!!!*******************************************')
                break

        html = BeautifulSoup(driver.page_source,"html.parser")            #获得完全加载的html，解析出数据

        books_list = html.find("div", {"id": "J_goodsList"}).findAll("li", {"class": "gl-item"})

        owner = '京东图书'
        typename = BookType.objects.get(typename__icontains=keyword)

        for book in books_list:
            title = book.find("div",{"class":"p-name"}) or book.find("div",{"class":"p-name p-name-type-2"})
            url = 'https://item.jd.com/%s.html' % book.attrs["data-sku"]
            price = book.find("div",{"class":"p-price"}).find("i").string
            loc = book.find("div",{"class":"p-shopnum"}) or book.find("div",{"class":"p-shop"})
            review = book.find("div",{"class":"p-commit"}).find("a").string
            photo = book.find("div",{"class":"p-img"}).find("img")

            try:
                photo = photo.attrs['src']
            except:
                photo =photo.attrs['data-lazy-img']

            if not loc:
                loc = "暂无"
            else:
                loc = loc.find("a")
                if not loc:
                    loc = "暂无"
                else:
                    loc = loc.attrs['title']

            if not title:
                title = "暂缺失数据"
            else:
                title = title.find("em")
                if not title:
                    title = "暂缺失数据"
                else:
                    title = title.get_text()

            if '万+' in review:
                review = float(review.split('万+')[0])*10000
                review += random.randint(1,4999)
            elif '+' in review:
                review = int(review.split('+')[0])
                review += random.randint(0,99)
            else:
                review = 0


            new_book = Book.objects.create(
                typename = typename,
                title=title,
                url=url,
                price=float(price),
                loc=loc,
                review=review,
                photo=photo,
                owner=owner
            )
            new_book.save()
            i += 1


        time.sleep(1)
        driver.find_element_by_css_selector("a[class='pn-next']").click()     #解析完成后点击下一页
        print("-"*1000)
        print(i)

    driver.quit()    #完成爬取后关闭浏览器
    print("爬完啦！✿✿ヽ(°▽°)ノ✿撒花")
        
        

