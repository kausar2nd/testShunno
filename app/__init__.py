from flask import Flask
from app.routes.user_routes import user_bp
from app.routes.company_routes import company_bp
from app.routes.admin_routes import admin_bp
from app.routes.general_routes import general_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "your secret key"

    # Register Blueprints
    app.register_blueprint(user_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(general_bp)

    return app
