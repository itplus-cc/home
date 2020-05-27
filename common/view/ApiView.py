# -*- coding: utf-8 -*-
from flask.views import MethodView
from flask import jsonify, request


class ApiView(MethodView):
    request = request

    def get(self):
        return jsonify("it is work get")

    def post(self):
        return jsonify("it is work post")

    def put(self):
        return jsonify("it is work put")

    def delete(self):
        return jsonify("it is work delete")

    def dispatch_request(self, *args, **kwargs):
        return super(ApiView, self).dispatch_request(*args, **kwargs)

    def response(self,code=0,data={},msg='',status=200):
        return jsonify({'code': code,'data':data,'msg': msg}), status


