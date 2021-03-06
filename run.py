from flask import Flask
from exts import db
from config import configs
from flask_cors import *
from flask_login import LoginManager
from apps.cms.models import CMSMember
import datetime
from flask_httpauth import HTTPBasicAuth


def create_app(develop):
    config_name = "develop"
    app = Flask(__name__)
    app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=10)
    CORS(app, supports_credentials=True)
    app.config["SECRET_KEY"] = 'TPmi4aLWRbyVq8zu9v82dWYW1'
    app.config.from_object(configs[config_name])
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'NetSecurity.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user = CMSMember.query.get(int(user_id))
        print('user', user)
        return user

    from apps.cms import bp as cms_bp
    app.register_blueprint(cms_bp)
    from apps.api_1_0 import bp as api_bp
    app.register_blueprint(api_bp)
    from apps.NetSecurity import bp as net_bp
    app.register_blueprint(net_bp)
    return app


if __name__ == '__main__':
    app = create_app("develop")
    app.run(port=8989, host='0.0.0.0')
