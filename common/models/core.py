import peewee as pe
from common import models as db

__all__ = ['Cate', 'Link']


class Cate(db.AbstractModel):
    name = pe.CharField(max_length=100, unique=True, verbose_name="name")
    icon = pe.CharField(max_length=100, default='', verbose_name="name")
    ishot = pe.BooleanField(default=False, verbose_name="常用推荐")
    pid = pe.IntegerField(default=0, index=True, verbose_name="上级")
    sort = pe.IntegerField(default=0, index=True, verbose_name="排序")

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'cate'


class Link(db.AbstractModel):
    name = pe.CharField(max_length=100, unique=True, verbose_name="name")
    desc = pe.CharField(max_length=100,  verbose_name="desc")
    icon = pe.CharField(max_length=200,  verbose_name="icon")
    url = pe.CharField(max_length=200,  verbose_name="icon")
    cate = db.ForeignKeyField(Cate, index=True, verbose_name="分类")

    def __str__(self):
        return f"{self.name}:{self.desc}"

    class Meta:
        db_table = 'link'
