# -*- coding:utf-8 -*-
"""
# Author:aluka_han
# Email:aluka_han@163.com
# Datetime:2019/8/30
# Reference: https://dormousehole.readthedocs.io/en/latest/patterns/fileuploads.html
# Description:
"""
import hashlib
# Standard library
import os
import tempfile
import time

import pymysql
# Third-party libraries
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, after_this_request, send_file
from flask import send_from_directory, jsonify

from src.dbutils.mysql_utils import Random_file

upload_folder = './file'  # 上传文件需要保存的目录
allowed_extensions = ['mp4']  # 允许上传的文件格式
app = Flask(__name__, template_folder='../templates')
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 上传文件的最大值


def allowed_file(filename):
    """
    上传文件的格式要求
    :param filename:文件名称
    :return:
    """
    return '.' in filename and \
        filename.rsplit('.')[1].lower() in allowed_extensions


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Please Select File')
            return redirect(url_for('upload'))
        f = request.files['file']
        if not allowed_file(f.filename):
            flash('Please Select Correct File')
            return redirect(url_for('upload'))
        if f and allowed_file(f.filename):
            h1 = hashlib.md5()
            h1.update((f.filename + str(round(time.time() * 1000))).encode(encoding='utf-8'))
            file_name = h1.hexdigest() + "." + f.filename.split('.')[1]
            save_path = os.path.join(app.config['UPLOAD_FOLDER'],
                                     secure_filename(file_name))
            f.save(save_path)
            insert_status = sql_file.insert_filename(file_name)
            if insert_status == '200':
                flash('Upload Success')
            else:
                flash(insert_status)
            # return redirect(url_for('show_upload_file', filename=secure_filename(f.filename)))
    return render_template('upload.html')


@app.route('/<filename>')
def show_upload_file(filename):
    """
    显示上传的文件并下载
    :param filename: 上传文件名称
    :return: 下载文件
    """
    sql_file.invalid_file(filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    # 创建一个临时文件
    with tempfile.TemporaryFile() as temp_file:
        with open(file_path, 'rb') as f:
            # 将上传的文件内容复制到临时文件中
            temp_file.write(f.read())

        @after_this_request
        def remove_file(response):
            """
            在返回响应后删除临时文件以及已下载的文件
            """
            temp_file.close()
            os.remove(file_path)
            return response

        return send_file(temp_file, as_attachment=True, download_name=filename)


@app.route('/get_one')
def get_one():
    """
    显示上传的文件并下载
    :param filename: 上传文件名称
    :return: 下载文件
    """
    file = sql_file.get_random_file()
    return {'code': 200, 'data': server_url + file["file"]}


if __name__ == '__main__':
    server_url = "http://127.0.0.1:9991/"
    sql_file = Random_file()
    app.run(host='0.0.0.0', port=9991, debug=True)
