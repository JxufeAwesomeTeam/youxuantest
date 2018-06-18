from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action


from .models import Share
from .serializer import BookShareSerializer

from apps.book.models import ISBNBook
from apps.login.models import User
from apps.login.jwt import verify_token
# Create your views here.
class BookShareViewSet(ReadOnlyModelViewSet):
    queryset = Share.objects.all()
    serializer_class = BookShareSerializer

    @csrf_exempt
    @action(methods=['post'],detail=False)
    def share(self,request):
        bid = int(request.POST.get('bid',None))
        uid = int(verify_token(request))
        text = request.POST.get('text',None)
        if text:
            try:
                new_share_book = ISBNBook.objects.get(id=bid)
                new_share_user = User.objects.get(id=uid)
            except:
                return Response('参数错误',status=400)
            else:
                new_share_share_text = text.encode('UTF-8')
                new_share = Share.objects.create(
                    book=new_share_book,
                    user=new_share_user,
                    share_text= new_share_share_text,
            )
                new_share.save()
            return Response('分享成功',status=200)
        else:
            return Response('分享内容不能为空',status=400)

    @csrf_exempt
    @action(methods=['get'],detail=False)
    def like(self,request):
        sid = request.GET.get('sid',None)
        if sid:
            share_obj = Share.objects.get(id=sid)
            share_obj.like += 1
            share_obj.save()
            return Response('点赞ok',status=200)
        else:
            return Response('参数错误',status=400)







