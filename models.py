from ext import db, app, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class baseModel:
    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def save(self):
        db.session.commit()



class Tour(db.Model, baseModel):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.ForeignKey("tour_category.id"))
    city = db.Column(db.String)
    country = db.Column(db.String) 
    price = db.Column(db.Float)
    img = db.Column(db.String)

    category_c = db.relationship("TourCategory")
    


class TourCategory(db.Model, baseModel):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String)

    tours = db.relationship("Tour")




class User (db.Model, baseModel, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)

    def __init__(self, username, password, role="normal"):
        self.username = username
        self.password = generate_password_hash(password)
        self.role = role
    
    def check_password(self, password):
        return check_password_hash(self.password, password)


@login_manager.user_loader    
def load_user(user_id):
    return User.query.get(user_id)
        



if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        foreign_country = TourCategory(country="foreign_country")
        db.session.add(foreign_country)
        db.session.commit()

        georgia = TourCategory(country="georgia")
        db.session.add(georgia)
        db.session.commit()


        new_user = User(username="admin", password="12345678", role="admin")
        new_user.create()





