
import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
           'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastname =db.Column(db.String(100))
    email = db.Column(db.String(50))
    jobTitle = db.Column(db.String(100))

    def __repr__(self) :
        return f"<Employee {self.firstName}>"

@app.route('/', methods=('POST', 'GET'))
def index():
    employees = Employee.query.all()
   
    return render_template('index.html', employees=employees,  )


@app.route('/login/', methods=('POST', 'GET'))
def login():
    
    if request.method== 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        jobTitle = request.form['jobtitle']
        newEmployee= Employee(firstName=firstname, lastname=lastname, email=email, jobTitle=jobTitle)
        db.session.add(newEmployee)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template('login.html')


@app.route('/update/<int:id>/', methods=('POST', 'GET'))
def update(id):
    empId = Employee.query.get_or_404(id)
    if request.method== 'POST':
        
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        jobTitle = request.form['jobtitle']
        empId.firstName = firstname
        empId.lastname = lastname
        empId.email = email
        empId.jobTitle = jobTitle
        db.session.add(empId)
        db.session.commit()
        return redirect(url_for("index"))
        
    return render_template('update.html', empId=empId, update=update)

@app.route("/delete/<int:id>/", methods=('POST', 'GET'))
def delete(id):
    empId = Employee.query.get_or_404(id)
    db.session.add(empId)
    db.session.delete(empId)
    db.session.commit()
    return redirect(url_for('index'))
