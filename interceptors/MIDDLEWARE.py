# -*- coding: utf-8 -*-
from app import app
from flask import request


@app.before_request
def before_request():
    if request.method == 'OPTIONS':
        return





@app.after_request
def after_request(response):
    return response



def checklogin():
   pass