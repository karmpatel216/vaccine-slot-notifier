from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from slot import VaccineSlot
from datetime import datetime
import pickle
from flask_mail import Mail, Message
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vaccine.db'
db = SQLAlchemy(app)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'getvaccineslot@gmail.com'
app.config['MAIL_PASSWORD'] = 'Vaccine@216'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)

current_path = os.getcwd()
with open(os.path.join(current_path,"slot","district_ids1.json"), "r") as fp:
    district_ids = json.load(fp)

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

@app.route("/",methods=["POST","GET"])
def home():
    db.create_all()
    states = district_ids.keys()
    if request.method == "POST":
        email = request.form["email"]
        by = request.form["by"]
        pin = request.form["pin"]
        state = request.form["state"]
        district = request.form["district"]
        age = request.form["age"]

        row = data(by=by, pin=pin,district=district,state=state,min_age=age,email=email)
        db.session.add(row)
        db.session.commit()

        #make a object
        date = datetime.today().date()
        day = str(date.day) if len(str(date.day)) == 2 else "0" + str(date.day)
        month = str(date.month) if len(str(date.month)) == 2 else "0" + str(date.month)
        year = str(date.year)
        date = f"{day}-{month}-{year}"
        min_age = 18 if age == "18-44" else 45
        info = {"date": date, "min_age":min_age}
        if by == "Area":
            info["by_district"] = 1
            info["state"] = state
            info["district"] = district
        else:
            info["by_district"] = 0
            info["pin"] = pin
        obj = VaccineSlot(info)

        objects = pickle.load(open(os.path.join(current_path,"pickleobjs"), "rb"))
        #objects = {}
        objects[email] = obj
        pickle.dump(objects, open(os.path.join(current_path,"pickleobjs"), "wb"))

        flash("you are sucessfully subscribed","success")
        return redirect(url_for("home"))

    return render_template("index.html",states=states)

@app.route("/district",methods=["POST","GET"])
def carbrand():

    if request.method == 'POST':
        state = request.form['state']
        #print(state)
        OutputArray = []
        districts = district_ids[state]
        for row in districts:
            outputObj = {
                'state': state,
                'district': row
            }
            OutputArray.append(outputObj)
        #print(OutputArray)
    return jsonify(OutputArray)


if __name__ == "__main__":
    app.run(debug=True,port=5002)