from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'mozartsecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mozart.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from .models import Usuario, Sessao, Mensagem  # Garante registro dos modelos
    from .routes import main
    app.register_blueprint(main)

    # Cria tabelas automaticamente se não existirem (dev only)
    with app.app_context():
        db.create_all()

    return app
