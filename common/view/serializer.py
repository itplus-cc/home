from peewee import *


class serializer(object):
    data = {}
    errlist = []

    def __init__(self, model=None, validated_data=None, ):
        self.model = model
        self.validated_data = validated_data

    def is_valid(self):
        self.errlist = []
        for field, obj in (self.get_field()).items():
            value = self.validated_data.get(field)
            if not value:
                if obj.primary_key:
                    continue
                if obj.null:
                    self.data[field] = obj.default if obj.default else None
                else:
                    if getattr(obj, 'default', None) is None:
                        self.errlist.append(f"{field} 不能为空")
            else:
                if isinstance(obj, BooleanField):
                    self.data[field] = value in ['1','true',True]
                else:
                    self.data[field] = value
        return False if self.errlist else True

    def update(self, instance=None):
        for field, obj in (self.get_field()).items():
            value = self.validated_data.get(field,None)
            if  value is None:
                continue
            setattr(instance, field, value)

        return instance

    def get_field(self):
        return self.model._meta.columns
