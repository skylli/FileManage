 # -*- coding: utf-8 -*-   

import os,json,logging,logger,uuid,time

from logger import log_conf
from flask import Flask, render_template, request, flash, redirect, render_template, session, abort,url_for,send_file,send_from_directory
from werkzeug import secure_filename

# import local file

from database import *

app = Flask(__name__)

log = log_conf(app.logger,logging.DEBUG)
# 文件 类
# 
# 获取脚本当前的目录 os.getcwd()
# 文件保存的路径,往往是绝对路劲
uuid_source = 'file.evalogik.com'
UPLOAD_FOLDER = os.getcwd()+'/store_file/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
PATH_RELATIVE = './store_file/'
#store_path = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/file_upload')
def file_upload():
    return render_template('file_upload.html')
	
@app.route('/file_uploading', methods = ['GET', 'POST'])
def file_uploading():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files: 
            flash('No file part')
            return redirect(url_for('file_upload'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        finputname = request.form['input_fname']
        if file.filename == ''or finputname is None:
            flash('No selected file')
            return redirect(url_for('file_upload'))
        if file:
            #产生随机序列
            uid = uuid.uuid3(uuid.NAMESPACE_DNS,uuid_source)
            # 添加后缀
            if file.filename is None:
                f_end = None
            else:
                f_end ='.' +  str(file.filename).split('.')[-1]
            # 文件名合法性
            fpath = secure_filename(str(int(time.time())) + '_' + str(uid)) + f_end
            log.debug("new filename is %s",fpath)
            # 文件上传
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], fpath))
            #  记录到数据库,记录相对路径
            path = '/' + fpath
            # 是否需要加后缀
            finputname += f_end
            fdb = File_db()
            log.info('file %s save to %s',finputname,path)
            fdb.file_add(file_idex = str(finputname),address= path,fname='test',filetype = 'pdf')
            return redirect(url_for('file_upload'))

@app.route('/file_find',methods = ['GET', 'POST'])
def file_find():
    key = request.form['input_search_key']
    find =  File_db().file_idex_search_key(key)
    return render_template('file_upload.html',output_filelist = find)

@app.route('/file_download',methods = ['GET', 'POST'])
def uploaded_file():
    filename = request.form['input_download_file']
    fname = File_db().file_address_get_by_idex(idex = filename)
    log.debug("file address --> %s",fname[0])
    return send_file(app.config["UPLOAD_FOLDER"] + str(fname[0]))

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=9527)
    log.warning('start to test')
