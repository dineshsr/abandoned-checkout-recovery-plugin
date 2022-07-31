from datetime import datetime

from flask import Flask, render_template, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CheckoutRecovery.db'
db = SQLAlchemy(app)


class SchedulesTemplate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    templateName = db.Column(db.String(200), nullable=False)
    schDetails = db.Column(db.String(2000), nullable=False)
    isDefault = db.Column(db.Boolean, nullable=False, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


class CartDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customerName = db.Column(db.String(200), nullable=False)
    itemCount = db.Column(db.String(2000), nullable=False)
    cxEmail = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


class OrderDetails(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customerName = db.Column(db.String(200), nullable=False)
    itemCount = db.Column(db.String(2000), nullable=False)
    cxEmail = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/schedules")
def schTemplates():
    return render_template("schTemplates.html")


@app.route("/addschedules", methods=['POST', 'GET'])
def addschedules():
    if request.method == 'POST':
        pass
    else:
        return render_template("addSchedule.html")


@app.route("/cartOrderDetails")
def showCartOrders():
    return render_template("cartorder.html")


@app.route("/schedulesForCart")
def schedulesForCart():
    return render_template("schedulesForCart.html")


@app.route("/addOrder", methods=['POST', 'GET'])
def addOrder():
    if request.method == 'POST':
        params = request.get_json();
        return {"status": "success"}
    else:
        return render_template("addOrder.html")


if __name__ == "__main__":
    app.run(debug=True, port=9090)
