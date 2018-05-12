from django.core.cache import cache

from .models import Book
def get_book_cache(id):
    '''
    尝试从缓存中通过id获取该书籍信息，若cache中不存在数据则从数据库读取，存入cache后返回data。

    :param title: 书名
    :return: Book对象
    '''
    key = id
    if cache.has_key(key):
        data = cache.get(key)

    else:
        data = Book.objects.get(id=id)
        cache.set(key,data,3600)
    return data

def set_book_cache():
    pass