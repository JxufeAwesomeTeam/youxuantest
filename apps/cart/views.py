from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin,DestroyModelMixin
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.

from .serializer import CartItemSerializer
from .models import  CartItem

from apps.login.models import User
from apps.login.jwt import verify_token
from apps.book.models import Book

class CartItemViewSet(RetrieveModelMixin,
                      DestroyModelMixin,
                      GenericViewSet):
    '''
    购物车item
    Retrieve:根据CartItem的id查询单个item
    Destroy:根据CartItem的id删除单个item 即删除购物车中item
    items: GET 根据当前登录用户id查询用户购物车item的所有items 即浏览整个购物车
           POST根据POST过来的bid与bcount来增加购物车的item 即加入购物车
    '''
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

    @csrf_exempt
    @action(methods=['get', 'post'],detail=False)
    def items(self, request):
        user_id = verify_token(request)
        if not user_id:
            return Response(data='请重新登录!', status=404)
        user = User.objects.get(id=user_id)

        if request.method == 'POST':
            book_id = int(request.POST.get('bid', None))
            quantity = int(request.POST.get('bcount', None)) or 1

            if not book_id and quantity and user_id:
                return Response(data='参数错误')
            else:
                try:
                    book = Book.objects.get(id=book_id)

                except:
                    return Response(data='未找到书籍', status=404)
                else:
                    try:
                        Item = CartItem.objects.get(
                            user=user,
                            book=book,
                        )
                    except:
                        newCartItem = CartItem.objects.create(
                            user=user,
                            book=book,
                            quantity=quantity
                        )
                        newCartItem.save()
                    else:
                        Item.quantity += quantity
                        Item.save()

        instances = CartItem.objects.filter(user=user)
        serializer = CartItemSerializer(instance=instances, many=True)
        return Response(data=serializer.data, status=200)











