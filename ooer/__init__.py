from flask import Flask
from flask_wtf import CSRFProtect


def create_application():
    application = Flask(__name__)

    import config
    application.config.from_object(config)

    CSRFProtect(application)

    from models import db
    db.init_app(application)

    with application.app_context():
        import blueprints
    for blueprint in blueprints.blueprints:
        application.register_blueprint(blueprint)

    import util
    util.init_utils(application)

    return application
