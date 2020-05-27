# -*- coding: utf-8 -*-

from flask import request
from flask.views import MethodView
from flask import render_template

class BaseView(MethodView):
    request = request

class BaseTemplateView(MethodView):
    template_name = ""
    request = request

    def get_context(self):
        return {}

    def get(self):
        context = self.get_context()
        return render_template(self.template_name, **context)



