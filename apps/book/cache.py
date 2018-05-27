from redis import Redis
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Book
from .serializer import BookSerializer

'''
当用户点击进入书籍商品详情页时：
前端发送一个GET请求，带上了该书籍商品bid；
后端通过redis的名为B_PV的hash保存这次点击操作 hset('B_PV', bid, book.pv + 1)
若B_PV已经存在key=bid的记录 则hincrby('B_PV', bid)
book的页面访问数(pv)自增1

'''
r = Redis()

def set_book_pv(request):
    """ 更新点击数 """
    bid = request.GET.get('bid',None)
    book = get_object_or_404(Book,id=bid)

    if book and bid:
        if r.hexists("B_PV", bid):
            r.hincrby('B_PV', bid)
        else:
            r.hset('B_PV', bid, 1)
        return HttpResponse('ok')
    else:
        return HttpResponse('不ok')

def get_book_pv(request):
    """ 获得点击数"""
    bcount = request.GET.get('bcount',10)
    Rank = []
    for k in r.hkeys('B_PV'):
        bid = int(k)
        book_click = int(r.hget('B_PV',bid))
        Rank.append((bid,book_click))

    rank = sorted(Rank, key=lambda x: x[1],reverse=True) #通过点击数排序

    rank_dict = {}
    for item in rank:
        rank_dict[item[0]] = item[1]

    import json
    rank_json = json.dumps(rank_dict) #返回json

    return HttpResponse(rank_json,status=200)