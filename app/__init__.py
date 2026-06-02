from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_wtf import CSRFProtect
db      = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt  = Bcrypt()
mail    = Mail()
csrf    = CSRFProtect()
def create_app(config_name: str = 'default') -> Flask:
    app = Flask(__name__)
    from .config import config
    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    csrf.init_app(app)
    login_manager.login_view     = 'main.login'
    login_manager.login_message  = 'Please sign in to access this page.'
    login_manager.login_message_category = 'warning'
    @login_manager.user_loader
    def load_user(user_id: str):
        from .models import User
        return User.query.get(int(user_id))
    from .routes import main
    app.register_blueprint(main)
    with app.app_context():
        _ensure_database(app)
    return app
def _ensure_database(app: Flask) -> None:
    import pymysql
    from .config import Config
    cfg = app.config
    host = cfg.get('_host') or 'localhost'
    port = int(cfg.get('_port') or 3306)
    uri = cfg['SQLALCHEMY_DATABASE_URI']
    import re
    m = re.match(r'mysql\+pymysql://([^:]+):([^@]*)@([^:/]+):?(\d+)?/([^?]+)', uri)
    if not m:
        return
    user, pw, host, port_str, dbname = m.groups()
    port = int(port_str or 3306)
    try:
        conn = pymysql.connect(host=host, port=port, user=user, password=pw)
        with conn.cursor() as cur:
            cur.execute(
                f"CREATE DATABASE IF NOT EXISTS `{dbname}` "
                "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
            )
        conn.commit()
        conn.close()
        app.logger.info(f"Database '{dbname}' ready.")
    except Exception as exc:
        app.logger.error(f"Could not ensure database exists: {exc}")
    try:
        db.create_all()
    except Exception as exc:
        app.logger.error(f"db.create_all() failed: {exc}")
