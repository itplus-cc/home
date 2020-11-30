from common.view.TemplateView import BaseTemplateView
from common.models.core import Cate, Link
import requests, json, datetime

__all__ = ["IndexView", "AdminView", "CateView", "LinkView"]


class IndexView(BaseTemplateView):
    template_name = "home/index.html"

    def get_context(self):
        context = super(IndexView, self).get_context()
        cates = (
            Cate.select(Cate.id, Cate.name, Cate.icon, Cate.ishot)
            .where(Cate.pid == 0)
            .order_by(Cate.sort.desc())
        )
        llist = list(cates.dicts())
        for x in llist:
            x["child"] = list(
                Cate.select(Cate.name, Cate.ishot)
                .where(Cate.pid == x["id"])
                .order_by(Cate.sort.desc())
                .dicts()
            )
        context["llist"] = llist
        rlist = list(Cate.select(Cate.id, Cate.name).order_by(Cate.sort.desc()).dicts())
        rlists = []
        for i, x in enumerate(rlist):
            links = list(Link.select().where(Link.cate == x["id"]).dicts())
            if links:
                x["child"] = links
                rlists.append(x)
        context["rlist"] = rlists
        return context


class AdminView(BaseTemplateView):
    template_name = "admin/index.html"


class CateView(BaseTemplateView):
    template_name = "admin/cate.html"

    def get_context(self):
        context = super(CateView, self).get_context()
        context["cates"] = Cate.select(Cate.id, Cate.name).where(Cate.pid == 0)
        return context


class LinkView(BaseTemplateView):
    template_name = "admin/link.html"

    def get_context(self):
        context = super(LinkView, self).get_context()
        context["cates"] = Cate.select(Cate.id, Cate.name)
        return context
