from flask import Flask
from flask_login import LoginManager

from routes import main_blueprint, session_scope
from db.database import init_db
from db.models import User
from config import settings


app = Flask(__name__)
app.register_blueprint(main_blueprint)
app.config['SECRET_KEY'] = settings.SECRET_KEY

login_manager = LoginManager(app)
login_manager.login_view = 'main.login'

@login_manager.user_loader
def load_user(user_id):
    with session_scope() as session:
        user = session.query(User).get(user_id)
        if user:
            session.expunge(user)
    return user    

if __name__ == '__main__':
    init_db()
    app.run(debug=True)