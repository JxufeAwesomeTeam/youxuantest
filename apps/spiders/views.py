from django.shortcuts import render,HttpResponse
from .spider import JDSpider,TBSpider,DDSpider
from apps.book.models import BookType
# Create your views here.

def Spider(request):
    return render(request,'spider.html')

def JDSpiderView(request,page):
    if not page:
        page = 1  #爬取多少页 每页有60个商品

    keywords = BookType.objects.all()

    for keyword in keywords:
        JDurl = "http://search.jd.com/bookadvsearch?keyword=%s&ep1=&ep2="
        JDSpider.crawl(JDurl, keyword.typename, page)
        print(keyword.typename+'类型已经爬完了'+str(page+1)+'页')
    return HttpResponse('Finish!')

def DDSpiderView(request,page):
    if not page:
        page = 1  #爬取多少页 每页有60个商品

    keywords = BookType.objects.all()

    DDurl = "http://search.dangdang.com/"

    for keyword in keywords:

        DDSpider.crawl(DDurl, keyword.typename, page)
        print(keyword.typename+'类型已经爬完了'+str(page+1)+'页')
    return HttpResponse('Finish!')

def TBSpiderView(request,page):
    if not page:
        page = 1  #爬取多少页 每页有44个商品

    keywords = BookType.objects.all()

    TBurl = "https://s.taobao.com/search"

    for keyword in keywords:
        TBSpider.crawl(TBurl, keyword.typename, page)
        print(keyword.typename+'类型已经爬完了'+str(page+1)+'页')
    return HttpResponse('Finish!')


from apps.book.models import Book,ISBNBook

def UnionISBN(request):
    books = Book.objects.all()
    ISBNbooks = ISBNBook.objects.all()
    for book in books:
        if not ISBNbooks.filter(ISBN=book.ISBN).exists():
            newISBNBook = ISBNBook.objects.create()
            newISBNBook.ISBN = book.ISBN
            newISBNBook.Books.add(book)
            newISBNBook.save()
        else:
            oldISBNBook = ISBNBook.objects.get(ISBN=book.ISBN)
            oldISBNBook.Books.add(book)
            oldISBNBook.save()

    #要是有重复的书要取最好的 去掉其他的 以京东的title为主title
    for book in ISBNbooks:
        #通过review排序
        items = book.Books.order_by('-review')
        owners =[]
        for item in items:
            if item.owner in owners:
                book.Books.remove(item)
                book.save()
            else:
                owners.append(item.owner)

    for book in ISBNbooks:
        items = book.Books.all()
        owners =[]
        for item in items:
            owners.append(item.owner)
        if 'JD' in owners:
            book.title = items.get(owner='JD').title
            book.photo = items.get(owner='JD').photo
        elif 'DD' in owners:
            book.title = items.get(owner='DD').title
            book.photo = items.get(owner='DD').photo
        else:
            book.title = items.get(owner='TM').title
            book.photo = items.get(owner='TM').photo
        book.save()
    return HttpResponse('finish')
