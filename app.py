from flask import Flask
from models import db
from routes import auth_bp
from config import Config
from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

jwt = JWTManager(app)

with app.app_context():
    db.create_all()
    
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    # debug mode only when testing.
    app.run(debug=True)