from flask import Blueprint

vcommon=Blueprint('vcommon',__name__)
@vcommon.route('/register' )
def register():
    return("succeed1")

@vcommon.route('/login')
def login():
    pass

