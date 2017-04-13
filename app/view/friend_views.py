from flask import Blueprint

vfriend=Blueprint('vfriend',__name__)

@vfriend.route('/get_friend_list/<user_id>')
def getFriendList(user_id):
    pass

@vfriend.route('/send_text')
def sendText():
    return('succeed2')

@vfriend.route('/send_friend_invitation')
def invitation():
    pass

@vfriend.route('/reply_invitation')
def reply_invitation():
    pass
