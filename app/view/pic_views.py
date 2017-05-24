from flask import Blueprint
import os
from flask import Flask, request, redirect, url_for,send_from_directory
from werkzeug.utils import secure_filename
from app.model.DBUtil import *
import json
vpic=Blueprint('vpic',__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
@vpic.route('/upload_pic',methods=['POST','GET'])
def uploadPic():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save('D:\\yue_server\\path\\' + filename)
            pic_id = DBUtil.insert_pic_url('D:\\yue_server\\path\\' + filename)
            dict = {'status': '1', 'pic_id': pic_id, 'errcode': "none"};
        else:
            dict = {'status': '0', 'pic_id': -1, 'errcode': "upload failed"};
    return json.dumps(dict)


@vpic.route('/get_pic_list/<activity_id>')
def getPicList(activity_id):
    pass


@vpic.route('/uploaded/<filename>')
def uploaded(filename):
    return send_from_directory('D:\\yue_server\\path\\',filename)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@vpic.route('/uploadtest',methods=['POST','GET'])
def upload_file():
        if request.method == 'POST':
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save('D:\\yue_server\\path\\'+filename)
                return redirect(url_for('vpic.uploaded', filename=filename))
                #return redirect("http://localhost:5000/uploads/"+filename)
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
          <p><input type=file name=file>
             <input type=submit value=Upload>
        </form>
        '''
@vpic.route("/get_pic/<pic_id>",methods=['POST','GET'])
def get_pic(pic_id):
    url=DBUtil.retrieve_avatar_url(pic_id)
    print(url)
    i = url.rindex("\\")
    pre = url[:i+1]
    print(pre)
    fname = url[i + 1:]
    print(fname)
    return send_from_directory(pre, fname)

@vpic.route("/testpic")
def testpic():
    pic_id = DBUtil.insert_pic_url('D:\\yue_server\\path\\' +"button9.png")
    return str(pic_id)

