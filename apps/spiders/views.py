from django.shortcuts import render ,HttpResponse
from .spider import JDSpider,TBSpider,DDSpider
from apps.book.models import BookType
# Create your views here.

def Spider(request):
    return render(request,'spider.html')

def JDSpiderView(request):

    page = 1  #爬取多少页 每页有60个商品

    keywords = BookType.objects.all()

    for keyword in keywords:
        JDurl = "http://search.jd.com/bookadvsearch?keyword=%s&ep1=&ep2="
        JDSpider.crawl(JDurl, keyword.typename, page)
        print(keyword.typename+'类型已经爬完了'+str(page+1)+'页')
    return HttpResponse('Finish!')

def DDSpiderView(request):

    page = 2

    keywords = BookType.objects.all()

    DDurl = "http://search.dangdang.com/"

    for keyword in keywords:

        DDSpider.crawl(DDurl, keyword.typename, page)
        print(keyword.typename+'类型已经爬完了'+str(page+1)+'页')
    return HttpResponse('Finish!')

def TBSpiderView(request):
    page = 2

    keywords = BookType.objects.all()

    TBurl = "https://s.taobao.com/search"

    for keyword in keywords:

        TBSpider.crawl(TBurl, keyword.typename, page)
        print(keyword.typename+'类型已经爬完了'+str(page+1)+'页')
    return HttpResponse('Finish!')