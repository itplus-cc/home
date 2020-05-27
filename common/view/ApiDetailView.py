from flask import request, jsonify, abort
from playhouse.shortcuts import model_to_dict
import traceback

from .serializer import serializer
from .ApiView import ApiView


class ApiDetailView(ApiView):
    model = ""
    request = request
    selectField = []
    pkField = ""

    def __init__(self):
        self.QuerySelectField = [getattr(self.model, x) for x in self.selectField]

    def get_object(self):
        pk = self.pkField if self.pkField else self.model.pk()
        pkvalue = self.request.args.get(pk)
        try:
            queryset = self.model.select(*self.QuerySelectField).where(getattr(self.model, pk) == pkvalue).get()
        except self.model.DoesNotExist as e:
            print(f'{e.__class__.__name__}: {e}')
            abort(404)
        return queryset

    def getAfter(self,obj):
        return obj

    def get(self):
        queryset = self.get_object()
        res = model_to_dict(queryset, only=self.QuerySelectField)
        res = self.getAfter(res)
        return jsonify({'code':0,'data':res})
    def postAfter(self,obj):
        pass
    def postBefore(self,postdata):
        return postdata
    def post(self):
        postdata=self.postBefore(self.request.get_json())
        seria = serializer(self.model, postdata)
        if not seria.is_valid():
            return jsonify({'code': -1, 'msg': "\n".join(seria.errlist)}), 500
        res = self.model(**seria.data)
        try:
            with self.model.trans() as txn:

                res.save()
                self.postAfter(res)
            return jsonify( {'code':0,'data':model_to_dict(res, only=self.QuerySelectField)}), 201
        except Exception as e:
            traceback.print_exc()
            print(f'{e.__class__.__name__}: {e}')
            return jsonify({'code': -1, 'msg': f'{e.__class__.__name__}: {e}'}), 500
    def putAfter(self,obj):
        return obj
    def put(self):
        self.QuerySelectField = []
        obj = self.get_object()
        obj = serializer(self.model, request.get_json()).update(obj)
        try:
            with self.model.trans() as txn:
                self.putAfter(obj)
                obj.save()
                return jsonify( {'code':0,'data':model_to_dict(obj, only=self.QuerySelectField)}), 201
        except Exception as e:
            traceback.print_exc()
            print(f'{e.__class__.__name__}: {e}')
            return jsonify({'code': -1, 'msg': f'{e.__class__.__name__}: {e}'}), 500

    def deleteAfter(self, obj):
        return obj
    def deleteBefore(self,obj):
        return obj
    def delete(self):
        obj = self.get_object()
        try:
            with self.model.trans() as txn:
                self.deleteBefore(obj)
                obj.delete_instance()
                self.deleteAfter(obj)
                return jsonify({'code':0,'msg':'ok'})
        except Exception as e:
            traceback.print_exc()
            print(f'{e.__class__.__name__}: {e}')
            return jsonify({'code': -1, 'msg': f'{e.__class__.__name__}: {e}'}), 500
