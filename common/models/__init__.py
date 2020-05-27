import peewee as pe
from app import db, database
from datetime import datetime

__all__ = ['BaseModel', 'AbstractModel','EnumField','ForeignKeyField']

class BaseModel(db.Model):
    """模型基类，为每个模型补充创建时间与更新时间"""
    id = pe.PrimaryKeyField()
    trans = database.atomic

    @classmethod
    def pk(self):
        return self._meta.primary_key.name

    @classmethod
    def fileds(self):
        fieldsDicts = self._meta.columns

        for field, obj in self._meta.columns.items():
            if isinstance(obj, ForeignKeyField):
                objconf = getattr(obj.Mmodel, '_meta')
                fieldsDicts = dict(fieldsDicts, **{f'{field}:{x}': v for x, v in objconf.columns.items()})
        return fieldsDicts

    @classmethod
    def getlist(self, selectFields=None):
        QuerySelectFields = []
        if selectFields:
            ownField = list(filter(lambda x: x in list(self._meta.columns.keys()), selectFields))
            if len(ownField) == 0:
                QuerySelectFields = [self, ]
            for i, v in self.fileds().items():
                if i in selectFields:
                    QuerySelectFields.append(v.alias(i))
        QuerySet = self.select(*QuerySelectFields)
        for field, obj in self._meta.columns.items():
            if isinstance(obj, ForeignKeyField):
                QuerySet = QuerySet.join(obj.Mmodel, on=(getattr(obj.Mmodel, obj.Mmodel.pk()) == getattr(self, field)))

        return QuerySet

    class Meta:
        database = database


class AbstractModel(BaseModel):
    create_time = pe.DateTimeField(default=datetime.now,  verbose_name='创建时间')  # 记录的创建时间
    update_time = pe.DateTimeField(default=datetime.now,  verbose_name='更新时间')  # 记录的更新时间

    def save(self, *args, **kwargs):
        """覆写save方法, update_time字段自动更新, 实例对象需要在update成功之后调用save()"""
        if self.pk() is None:
            # this is a create operation, set the date_created field
            self.create_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return super(BaseModel, self).save(*args, **kwargs)


class EnumField(pe.SmallIntegerField):
    """
    This class enable an Enum like field for Peewee
    """

    def __init__(self, choices, *args, **kwargs):
        super(EnumField, self).__init__(*args, **kwargs)
        self.choices = choices

    def db_value(self, value):
        choiceslist = [x[1] for x in self.choices]
        valueslist = [x[0] for x in self.choices]
        if value in choiceslist:
            return self.choices[choiceslist.index(value)][0]
        if value in valueslist:
            return self.choices[valueslist.index(value)][0]
        raise Exception(f" {value} not in choices")

    def python_value(self, value):
        return self.choices[value][1]


class ForeignKeyField(pe.IntegerField):
    """
    This class enable an Enum like field for Peewee
    """

    def __init__(self, Mmodel, selectField=[], *args, **kwargs):
        self.Mmodel = self if Mmodel == 'self' else Mmodel
        self.QuerySelectField = [getattr(self.Mmodel, x) for x in selectField]
        super(ForeignKeyField, self).__init__(*args, **kwargs)

    def db_value(self, value):
        try:
            obj = self.Mmodel.select(getattr(self.Mmodel, self.Mmodel.pk())).where(
                getattr(self.Mmodel, self.Mmodel.pk()) == value).get()
            return obj.id
        except pe.DoesNotExist:
            raise Exception(f"{self.Mmodel._meta.table_name}:{value} is does not exist")

    def python_value(self, value):
        return value



