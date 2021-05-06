from app import db

class data(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    by = db.Column(db.String(20), unique=False, nullable=False)
    pin = db.Column(db.String(20), unique=False, nullable=True)
    district = db.Column(db.String(50), unique=False, nullable=True)
    state = db.Column(db.String(50), unique=False, nullable=True)
    min_age = db.Column(db.String(10), unique=False, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)


    def __repr__(self):
        return f"Data('{self.email}','{self.min_age}','{self.by}')"