import requests
import re
import pymysql
from bs4 import BeautifulSoup

from apps.book.models import BookType, Book


def crawl(start_url,keyword,maxpage):

    payload = {'key': keyword, 'category_path': '01.00.00.00.00.00', 'page_index': 1}

    for page in range(maxpage):

        resp = requests.get(start_url, params=payload)

        payload['page_index'] = page + 2  # 下一页

        print(payload['page_index'])
        bsObj = BeautifulSoup(resp.text, 'lxml')

        goods = bsObj.find("ul", {"class": "bigimg"}).findAll("li")

        owner = '当当图书'
        typename = BookType.objects.get(typename__icontains=keyword)
        for good in goods:
            title = good.find("a", {"class": "pic", "name": "itemlist-picture"}).attrs['title']
            price = good.find("p", {"class": "price"}).find("span", {"class": "search_now_price"}).string[1:]
            url_id = good.attrs['id'][1:]  # 去掉P id = p23746255
            url = good.find("a", {"class": "pic", "name": "itemlist-picture"}).attrs['href']
            loc = good.find("a", {"name": "P_cbs"})
            photo = good.find("a",{"class": "pic", "name": "itemlist-picture"}).find("img")
            review = good.find("p",{"class":"search_star_line"}).find("a").string
            if not loc:
                loc = "暂无"
            else:
                loc = loc.string

            try:
                photo = photo.attrs['data-original']
            except:
                photo = photo.attrs['src']


            if '条评论' in review:
                review = int(review.split('条评论')[0])
            else:
                review = 0
            new_book = Book.objects.create(
                typename=typename,
                title=title,
                url=url,
                price=float(price),
                loc=loc,
                review=review,
                photo=photo,
                owner=owner
            )
            new_book.save()

    print("爬完啦！✿✿ヽ(°▽°)ノ✿撒花")


