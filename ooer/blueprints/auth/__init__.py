from flask import current_app, Blueprint
from flask_login import LoginManager

from ooer.models.user import User

login_manager = LoginManager()

login_manager.login_view = 'auth.login'
login_manager.login_message = u'Please log in to access this page.'
login_manager.login_message_category = 'info'

login_manager.refresh_view = 'auth.reauth'
login_manager.needs_refresh_message = u'To protect your account, please reauthenticate to access this page.'
login_manager.needs_refresh_message_category = 'info'


@login_manager.user_loader
def user_loader(id):
    return User.objects(id=id).first()


login_manager.init_app(current_app, add_context_processor=True)

blueprint = Blueprint('auth', __name__)

from views import login, logout, forums
