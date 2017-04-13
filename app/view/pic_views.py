from flask import Blueprint

vpic=Blueprint('vpic',__name__)
@vpic.route('/get_pic/<pic_id>' )
def getPic(pic_Id):
   pass

@vpic.route('/upload_pic')
def uploadPic():
    pass

@vpic.route('/get_pic_list/<activity_id>')
def getPicList(activity_id):
    pass

