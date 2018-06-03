import requests
import re
from bs4 import BeautifulSoup

from apps.book.models import BookType, Book


def crawl(start_url,keyword,maxpage):

    payload = {'key': keyword, 'category_path': '01.00.00.00.00.00', 'page_index': 1}

    #爬取多少页
    for page in range(maxpage):

        headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.139 Mobile Safari/537.36'}
        resp = requests.get(start_url, params=payload, headers=headers)

        payload['page_index'] = page + 2  # 下一页
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
            
            r = requests.get(url,headers=headers)

            detail = BeautifulSoup(r.text,'lxml')
            msg = detail.find('ul',{'class':'key clearfix'})

            if msg:
                try:
                    ISBN = int(re.findall(r'国际标准书号ISBN：([\d]+)', msg.text)[0])
                except:
                    ISBN = 0
            else:
                try:
                    ISBN = int(re.findall(r'ISBN","content":"([\d]+)"', detail.text)[0])
                except:
                    ISBN = 0
            # 如果已经存在则视为更新 否则为新建
            try:
                update_book = Book.objects.get(url=url)
            except:
                new_book = Book.objects.create(
                    typename=typename,
                    title=title,
                    url=url,
                    price=float(price),
                    loc=loc,
                    review=review,
                    photo=photo,
                    owner=owner,
                    ISBN=ISBN
                )
                new_book.save()
            else:
                #更新一般的是价格、标题、图片、评论数
                update_book.title = title
                update_book.price = price
                update_book.photo = photo
                update_book.review = review
                update_book.save()

    print("爬完啦！✿✿ヽ(°▽°)ノ✿撒花")


