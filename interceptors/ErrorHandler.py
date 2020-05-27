# -*- coding: utf-8 -*-

from app import app
from flask import jsonify

@app.errorhandler(404) #捕获应用的异常
def error_404(e):
    return jsonify(),404

@app.errorhandler(500) #捕获应用的异常
def error_500(e):
    return jsonify(),500

@app.errorhandler(502) #捕获应用的异常
def error_502(e):
    return jsonify(),502

@app.errorhandler(403) #捕获应用的异常
def error_403(e):
    print(e)
    return jsonify(),403


