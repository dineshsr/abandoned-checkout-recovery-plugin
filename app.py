from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
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


@app.route("/addschedules")
def addschedules():
    return render_template("addSchedule.html")


@app.route("/cartOrderDetails")
def showCartOrders():
    return render_template("cartorder.html")


@app.route("/schedulesForCart")
def schedulesForCart():
    return render_template("schedulesForCart.html")


@app.route("/addOrder")
def addOrder():
    return render_template("addOrder.html")


if __name__ == "__main__":
    app.run(debug=True, port=9090)
