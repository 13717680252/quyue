from flask import Blueprint
import os
from flask import Flask, request, redirect, url_for,send_from_directory
from werkzeug.utils import secure_filename

vpic=Blueprint('vpic',__name__)
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
@vpic.route('/get_pic/<pic_id>' )
def getPic(pic_Id):
   pass

@vpic.route('/upload_pic')
def uploadPic():
    pass

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

