import requests
import re
import pymysql
from bs4 import BeautifulSoup

from apps.book.models import BookType, Book


def crawl(start_url,keyword,maxpage):
    payload = {'q': keyword, 's': '1', 'cat': '33'}

    for page in range(maxpage):
        payload['s'] = 44 * page + 1
        print(payload)
        headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'}

        resp = requests.get(start_url, params=payload,headers=headers)

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
        typename = BookType.objects.get(typename__icontains=keyword)


        for i in range(len(title)):
            if '人付款' in review[i]:
                review_item = int(review[i].split('人付款')[0])
            else:
                review_item = 0
            if url_id[i] in url[i]:
                real_url = 'https://detail.tmall.com/item.htm?id='+str(url_id[i])
            else:
                real_url = 'https:'+url[i].replace('\\u003d','=').replace('\\u0026','&')
            r = requests.get(real_url,headers=headers)
            r.encoding = 'ISO-8859-1'
            msg = BeautifulSoup(r.text,'lxml')
            try:
                ISBN = int(re.findall(r'"ISBN±àºÅ":"([^"]+)"', msg.text)[0])

                print(ISBN)
            except:
                ISBN = 0


            try:
                update_book = Book.objects.get(url=real_url)
            except:
                new_book = Book.objects.create(
                    typename=typename,
                    title=title[i],
                    url=real_url,
                    price=price[i],
                    loc=loc[i],
                    review=review_item,
                    photo=photo[i],
                    owner=owner,
                    ISBN=ISBN
                )
                new_book.save()
            else:
                #更新一般的是价格、标题、图片、评论数
                update_book.title = title[i]
                update_book.price = price[i]
                update_book.photo = photo[i]
                update_book.review = review_item
                update_book.save()

    print("爬完啦！✿✿ヽ(°▽°)ノ✿撒花")
