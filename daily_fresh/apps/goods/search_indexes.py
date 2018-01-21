from haystack import indexes
from .models import GoodsSKU


# 指定对于某个类的某些数据建立索引
class GoodsSKUIndex(indexes.SearchIndex, indexes.Indexable):
    # 索引字段   use_template=True说明在一个文件中指定根据表中哪些字段内容建立索引数据
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return GoodsSKU

    # 返回哪些数据就会对他们建立索引
    def index_queryset(self, using=None):
        return self.get_model().objects.all()