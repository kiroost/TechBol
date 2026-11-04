
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configuración
    app.config['SECRET_KEY'] = 'techbot-secreto'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///techbot.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    Bootstrap(app)

    # Importar modelos
    from app import models

    # Registrar Blueprints
    from app.clientes import bp_clientes
    from app.productos import bp_productos
    from app.pedidos import bp_pedidos

    app.register_blueprint(bp_clientes, url_prefix='/clientes')
    app.register_blueprint(bp_productos, url_prefix='/productos')
    app.register_blueprint(bp_pedidos, url_prefix='/pedidos')

    @app.route('/')
    def inicio():
        return render_template('index.html')

    return app
