from common.view import ApiView, ApiDetailView, ApiListView
from common.models.core import Cate, Link
from playhouse.shortcuts import model_to_dict
from werkzeug.utils import secure_filename
from flask import jsonify
import datetime,os
__all__ = [
    'CateApi', 'CatesApi',
    'LinkApi', 'LinksApi',
    'IconUploadApi'
]


class CateApi(ApiDetailView):
    model = Cate

    def deleteBefore(self, obj):
        p = Cate.get_or_none(Cate.pid == obj.id)
        l = Link.get_or_none(Link.cate == obj.id)
        if p :
            raise Exception('存在子分类')
        if l:
            raise Exception('存在关联链接')


class CatesApi(ApiListView):
    model = Cate
    filterField = []
    searchField = []
    selectField = []
    orderField = ['id', 'create_time']
    ordering = '-sort'
    pagesize = 10
    page = 1

    def getAfter(self, obj):
        for x in obj:
            if x['pid'] != 0:
                c = Cate.get_or_none(Cate.id == x['pid'])
                pid = model_to_dict(c) if c else 'error'
                x['pid'] = pid
            else:
                x['pid'] = 0
        return obj


class LinkApi(ApiDetailView):
    model = Link

class LinksApi(ApiListView):
    model = Link
    filterField = []
    searchField = []
    selectField = []
    orderField = ['id', 'create_time']
    ordering = '-create_time'
    pagesize = 10
    page = 1


def getdirname():
    x = datetime.datetime.now()
    basedir=f"{os.getcwd()}/static/upload/{x.year}/{x.month}/{x.day}/"
    if not os.path.exists(basedir):
        os.makedirs(basedir)
    return  basedir,f"/static/upload/{x.year}/{x.month}/{x.day}/"

class IconUploadApi(ApiView):
    def post(self):
        files = self.request.files
        print(files)
        if not files:
            return jsonify({
               'code':-1,
                'msg':'文件不存在'
            })

        file = files['file']
        filename = secure_filename(file.filename)
        if file and file.mimetype in ['image/jpeg', 'image/png']:
            filename = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f') + os.path.splitext(filename)[-1]
            try:
                dirpath, url = getdirname()
                file.save(os.path.join(dirpath, filename))
                return jsonify({
                    'code': 0,
                    'data': url + filename
                })
            except Exception as e:
                print(e)
                return jsonify({
                    'code': -1,
                    'msg': e
                })
        else:
            return jsonify({
                'code': -1,
                'msg': '错误的文件类型'
            })

