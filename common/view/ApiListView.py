from flask import request, jsonify, abort
from operator import or_
from functools import reduce
import traceback

from .ApiView import ApiView


class ApiListView(ApiView):
    filterField = []
    searchField = []
    selectField = []
    orderField = []
    ordering = None
    model = None
    request = request
    pagesize = 10
    page = 1

    def __init__(self):
        self.selectField = self.request.values.getlist("selectField[]") if self.request.values.getlist(
            "selectField[]") else self.selectField
        self.ordering = self.request.values.get("ordering") if self.request.values.get(
            "ordering") else self.ordering

    def get_quertset(self):

        queryset = self.model.getlist(self.selectField)
        searchValue = self.request.values.get("searchvalue")

        if searchValue and self.searchField:
            searchlist = []

            for x in self.searchField:
                list = x.split(":")
                if len(list) == 2:
                    fieldMode = getattr(self.model, list[0])
                    searchlist.append(getattr(fieldMode.Mmodel, list[1]).contains(str(searchValue)))
                else:
                    searchlist.append(getattr(self.model, x).contains(str(searchValue)))

            queryset = queryset.where(
                reduce(or_, searchlist))
        filterQuery = []
        for field in self.filterField:

            value = self.request.values.get(field)
            if value:
                # filterQuery.append(reduce(eq, [getattr(self.model, field), value]))
                notin = False
                if value[0] == "!":
                    notin = True
                    value = value[1:]
                list = field.split(":")
                if len(list) == 2:
                    fieldMode = getattr(self.model, list[0])
                    if notin:
                        filterQuery.append(getattr(fieldMode.Mmodel, list[1]).not_in(str(value).split("|")))
                    else:
                        filterQuery.append(getattr(fieldMode.Mmodel, list[1]).in_(str(value).split("|")))
                else:
                    if notin:
                        filterQuery.append(getattr(self.model, field).not_in(str(value).split("|")))
                    else:
                        filterQuery.append(getattr(self.model, field).in_(str(value).split("|")))

        if filterQuery:
            queryset = queryset.where(*filterQuery)
        print(queryset)
        if self.ordering and self.orderField:
            desc = True if "-" in self.ordering else False
            order = self.ordering[1:] if "-" in self.ordering else self.ordering
            if order in self.orderField:
                fieldCls = getattr(self.model, order)
                queryOrder = getattr(fieldCls, "desc")() if desc else getattr(fieldCls, "asc")()
                queryset = queryset.order_by(queryOrder)
        count = queryset.count()
        if self.request.values.get("isAll"):
            return queryset, count
        _pagesize = self.request.values.get('pagesize', self.pagesize)
        page = self.request.values.get('page', self.page)
        self.pagesize = _pagesize if int(_pagesize) < 100 else self.pagesize
        queryset = queryset.paginate(int(page), int(self.pagesize))
        return queryset, count

    def getAfter(self, obj):
        return obj

    def get(self):
        try:
            queryset, count = self.get_quertset()
        except Exception as e:
            traceback.print_exc()
            print(f'{e.__class__.__name__}: {e}')
            return jsonify({'code': -1, 'msg': f'{e.__class__.__name__}: {e}'}), 500
        res = list(queryset.dicts())
        res = self.getAfter(res)
        return jsonify({'code':0,'data':{'count': count, 'results': res, 'pagesize': self.pagesize}})

    def post(self):
        abort(404)

    def put(self):
        setvalue = self.request.get_json().get("value")
        setvalueKey = list(filter(lambda x: x in self.model._meta.columns and setvalue[x], list(setvalue.keys())))
        query = self.request.get_json().get("query")
        queryKey = list(filter(lambda x: x in self.model._meta.columns and query[x], list(query.keys())))
        queryset = self.model.update(**{x: setvalue[x] for x in setvalueKey}).where(
            *[getattr(self.model, x).in_(query[x]) for x in queryKey])
        try:
            with self.model.trans():
                queryset.execute()
            return jsonify({'code': 0, 'msg': 'ok'})
        except Exception as e:
            traceback.print_exc()
            print(f'{e.__class__.__name__}: {e}')
            return jsonify({'code': -1, 'msg': f'{e.__class__.__name__}: {e}'}), 500

    def get_object(self):
        pk = self.pkField if self.pkField else self.model.pk()
        pkvalue = self.request.args.get(pk)
        try:
            queryset = self.model.select().where(getattr(self.model, pk) == pkvalue).get()
        except self.model.DoesNotExist as e:
            print(f'{e.__class__.__name__}: {e}')
            abort(404)
        return queryset

    def delete(self):
        pkvalue = self.request.args.get(self.model.pk())
        queryset = self.model.delete().where(getattr(self.model, self.model.pk()) == pkvalue)
        try:
            queryset.execute()
            return jsonify({'code': 0, 'msg': 'ok'})
        except Exception as e:
            traceback.print_exc()
            print(f'{e.__class__.__name__}: {e}')
            return jsonify({'code': -1, 'msg': f'{e.__class__.__name__}: {e}'}), 500
