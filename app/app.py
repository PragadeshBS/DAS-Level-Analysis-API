from flask import Flask, Blueprint, request, jsonify, render_template
from app import dsa
import os
import requests

bp=Blueprint('app',__name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/api/analyze',methods=['POST','GET'])
def dsaResult():
    if request.method=='POST':
        text=request.form['text']
        lst=dsa.ret_results(text)
        print(lst)
        result={'depression':str(lst[0]),'anxiety':str(lst[1]),'stress':str(lst[2])}
        return jsonify(result)