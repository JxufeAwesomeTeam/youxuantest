from django.db import models

# Create your models here.
class BookType(models.Model):

    typename = models.CharField(max_length=100,unique=True,verbose_name="类型名")

    class Meta:
        verbose_name = "书籍类型"
        verbose_name_plural = "书籍类型"

    def __str__(self):
        return self.typename

Choices =(
    ('DD','当当图书'),
    ('TB','淘宝图书'),
    ('JD','京东图书'),
)
class Book(models.Model):

    typename = models.ForeignKey(BookType,related_name='bookType',on_delete=models.DO_NOTHING,verbose_name="标签")
    title = models.CharField(max_length=255,verbose_name="标题")
    url = models.URLField(max_length=1000,verbose_name="网址")
    price = models.DecimalField(default=0.00,decimal_places=2,max_digits=10,verbose_name="价格")
    loc = models.CharField(default='暂无',max_length=255,verbose_name="作者/出版社")
    review = models.IntegerField(default=0,verbose_name="评论数")
    photo = models.URLField(max_length=1000,verbose_name="图片名")
    owner = models.CharField(choices=Choices,default='当当书城',max_length=255,verbose_name='所属书城')
    ISBN = models.CharField(default=0,max_length=14,verbose_name='ISBN')

    class Meta:
        verbose_name = "书籍"
        verbose_name_plural = "书籍"

    def __str__(self):
        return self.title

class ISBNBook(models.Model):
    ISBN = models.CharField(default=0, max_length=14, verbose_name='ISBN')
    Books = models.ManyToManyField(Book,verbose_name='书籍')
    title = models.CharField(default='暂无',max_length=255,verbose_name='标题')
    photo = models.URLField(default='暂无',max_length=1000,verbose_name='图片名')