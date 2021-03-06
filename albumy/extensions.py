
from flask_mail import Mail
from flask_moment import Moment
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_login import AnonymousUserMixin
from flask_dropzone import Dropzone
from flask_avatars import Avatars
from flask_whooshee import Whooshee


mail = Mail()
moment = Moment()
db = SQLAlchemy()
csrf = CSRFProtect()
ckeditor = CKEditor()
bootstrap = Bootstrap()
migrate = Migrate(db=db)
login_manager = LoginManager()
dropzone = Dropzone()
avatars = Avatars()
whooshee = Whooshee()

login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'warning'
login_manager.login_message = '请先登录'
login_manager.refresh_view = 'auth.re_authenticate'
login_manager.needs_refresh_message = u'为了保护你的账号安全, 请重新登陆'


@login_manager.user_loader
def load_user(user_id):
    from albumy.models import User
    user = User.query.get(int(user_id))
    return user


class Guest(AnonymousUserMixin):
    @property
    def is_admin(self):
        return False

    def can(self, permission_name):
        return False


login_manager.anonymous_user = Guest



