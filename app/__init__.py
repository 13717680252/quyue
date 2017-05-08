from flask import Flask
import pymysql
pymysql.install_as_MySQLdb()
from app.view.friend_views import vfriend
from app.view.activity_views import *
from app.view.common_views import *
from app.view.group_views import *
from app.view.group_views import *
from app.view.pic_views import *
from app.view.user_views import *

app = Flask(__name__)
app.config.from_object("config")
app.register_blueprint(vfriend)
app.register_blueprint(vactivity)
app.register_blueprint(vcommon)
app.register_blueprint(vgroup)
app.register_blueprint(vpic)
app.register_blueprint(vuser)



from app.view import *