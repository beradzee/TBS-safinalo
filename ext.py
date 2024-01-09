from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "L1S+7@Xz\Pr8_AP9#!)V@`*<"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"




db = SQLAlchemy(app)

login_manager = LoginManager(app)


login_manager.login_view = "sign_in"