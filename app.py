from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sendEmail import sendEmail
from sqlalchemy.sql import func

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:571612@localhost/height_collector'
db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__="data"
    id=db.Column(db.Integer, primary_key=True)
    email=db.Column(db.String(120), unique= True)
    height= db.Column(db.Integer)
    
    def __init__(self, email, height):
        self.email= email
        self.height= height



@app.route("/")
def index():
    return render_template("index.html")

@app.route("/success", methods=['POST'])
def success():
    if request.method == 'POST':
        inputEmail= request.form["email_name"]
        inputHeight= request.form["height_name"]
        sendEmail(inputEmail, inputHeight)

        # Checking for duplicated email
        if db.session.query(Data).filter(Data.email == inputEmail).count() == 0:
            #creating an object and passing the variables as arguments for the constructor 
            data = Data(inputEmail, inputHeight)
            db.session.add(data)
            db.session.commit()
            averageHeight = db.session.query(func.avg(Data.height)).scalar()
            averageHeight= round(averageHeight)
            count = db.session.query(Data.height).count()
            sendEmail(inputEmail, inputHeight, averageHeight, count)
            return render_template("success.html")
    return render_template('index.html', text="This email has already been used. Try another one.")
            


if __name__ == '__main__':
    app.debug = True
    app.run()
