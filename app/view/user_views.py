from flask import Blueprint

vuser=Blueprint('vuser',__name__)
@vuser.route('/get_user_info/<user_id>')
def getUserInof(user_id):
  pass

@vuser.route('/get_credit_list/<user_id>')
def getCreditList(user_id):
    pass

@vuser.route('/change_password/<user_id>')
def changePassword(user_id):
    pass

@vuser.route('/change_my_info/<user_id>')
def changeInfo(user_id):
    pass

