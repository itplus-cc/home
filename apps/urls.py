from flask import Blueprint
from .core.views import IndexView,AdminView,CateView,LinkView


import importlib


AUTOAPI_MODULES = (
    'core',
)

def addUrlRule(route, Rules):
    for path, name, func in Rules:
        route.add_url_rule(path, view_func=func.as_view(name))


route_index = Blueprint('core', __name__)
route_api = Blueprint('api', __name__)

route_index.add_url_rule('/', view_func=IndexView.as_view('index'))
route_index.add_url_rule('/admin', view_func=AdminView.as_view('admin'))
route_index.add_url_rule('/cate', view_func=CateView.as_view('cate'))
route_index.add_url_rule('/link', view_func=LinkView.as_view('link'))

for m in AUTOAPI_MODULES:
    modules = importlib.import_module(f'apps.{m}.api')
    for cls in modules.__all__:
        func = getattr(modules, cls)
        route_api.add_url_rule(cls, view_func=func.as_view(cls))
