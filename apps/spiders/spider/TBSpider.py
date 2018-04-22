import requests
import re
import pymysql
from bs4 import BeautifulSoup

from apps.book.models import BookType, Book


def crawl(start_url,keyword,maxpage):
    payload = {'q': keyword, 's': '1', 'cat': '33'}

    for page in range(maxpage):
        payload['s'] = 44 * page + 1

        resp = requests.get(start_url, params=payload)

        resp.encoding = 'UTF-8'

        # bsObj = BeautifulSoup(resp.text, 'lxml')

        title = re.findall(r'"raw_title":"([^"]+)"', resp.text, re.I)
        price = re.findall(r'"view_price":"([^"]+)"', resp.text, re.I)
        review =re.findall(r'"view_sales":"([^"]+)"', resp.text, re.I)
        url_id = re.findall(r'"nid":"([^"]+)"', resp.text, re.I)
        photo = re.findall(r'"pic_url":"([^"]+)"', resp.text, re.I)
        url = re.findall(r'"detail_url":"([^"]+)"', resp.text, re.I)
        loc = re.findall(r'"nick":"([^"]+)"', resp.text, re.I)
        owner = '天猫图书'

        for i in range(len(title)):
            typename = BookType.objects.get(typename__icontains=keyword)
            new_book = Book.objects.create(
                typename=typename,
                title=title[i],
                url=url[i],
                price=price[i],
                loc=loc[i],
                review=review[i],
                photo=photo[i],
                owner=owner,
            )
            new_book.save()

    print("爬完啦！✿✿ヽ(°▽°)ノ✿撒花")
