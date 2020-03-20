import os
import json

from flask import Flask
from flask import redirect
from flask import render_template
from flask import request
from flask import jsonify

from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:TANYUSHAN@localhost/test'

db = SQLAlchemy(app)

class Student(db.Model):
    student_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    amount_due = db.Column(db.Integer)
    def __repr__(self):
        return str(self.__dict__)


# For Show all records
@app.route('/', methods=["GET"])
def home():    
    students = Student.query.all()
    return render_template("home.html", students=students)

# For Read
@app.route("/read/<id>",  methods=["GET"])
def read(id):
    try:
        student = Student.query.filter_by(student_id=id).first()
        print(student)
    except Exception as e:
        print("Failed to add Student")
        print(e)
    print(student) 
    return 'Student ID:' + student.student_id + ' ' + student.first_name + ' ' + student.last_name

# For Create
@app.route("/create", methods=["POST"])
def create():
    try:
        student = Student(student_id=request.form.get("student_id"), 
                          first_name=request.form.get("first_name"), 
                          last_name=request.form.get("last_name"),
                          amount_due=request.form.get("amount_due"),
                          )
        print(student)
        db.session.add(student)
        db.session.commit()
    except Exception as e:
        print("Failed to add Student")
        print(e)
    return redirect("/")

# For Update
@app.route("/update", methods=["POST"])
def update():
    try:
        new_amount = request.form.get("new_amount")
        old_id = request.form.get("old_id")
        print(old_id)
        student = Student.query.filter_by(student_id=old_id).first()
        student.amount_due = new_amount
        db.session.commit()
    except Exception as e:
        print("Couldn't update student")
        print(e)
    return redirect("/")

# For delete
@app.route("/delete", methods=["POST"])
def delete():
    student_id = request.form.get("student_id")
    student = Student.query.filter_by(student_id=student_id).first()
    db.session.delete(student)
    db.session.commit()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)