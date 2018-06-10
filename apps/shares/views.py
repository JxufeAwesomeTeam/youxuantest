from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.decorators import action


from .models import Share
from .serializer import BookShareSerializer

from apps.book.models import Book
from apps.login.models import User
from apps.login.jwt import verify_token
# Create your views here.
class BookShareViewSet(ReadOnlyModelViewSet):
    queryset = Share.objects.all()
    serializer_class = BookShareSerializer

    @action(methods=['post'],detail=True)
    def share(self,request):
        bid = request.POST.get('bid',None)
        uid = verify_token(request)
        text = request.POST.get('text',None)
        if text:
            try:
                new_share = Share.objects.create()
                new_share.book = Book.objects.get(id=bid)
                new_share.user = User.objects.get(id=uid)
            except:
                return Response('参数错误！')
            else:
                new_share.share_text = text.encode('UTF-8')
                new_share.save()
        else:
            return Response('分享内容不能为空！')


    @action(methods=['get'],detail=True)
    def like(self,request):
        pass






