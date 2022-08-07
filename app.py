import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, g
from flask_cors import CORS

from database import get_db

app = Flask(__name__)
cors = CORS(app)
sched = BackgroundScheduler(daemon=True)
sched.start()
JOB_TYPE = 'date'
SELECT_ORDERS = "select * from OrderDetails"
SELECT_CARTS = "select * from CartDetails"
SELECT_SCHEDULES = "select * from ScheduleTemplate"

DUMMY_DATA = {
    "customerName": "abc",
    "itemCount": 10,
    "cxEmail": "abc@gmail.com",

}


@app.teardown_appcontext
def close_db(error):
    '''when the flask app stops, the db is closed'''
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/schedules")
def schTemplates():
    return render_template("schTemplates.html")


@app.route("/addschedules", methods=['POST', 'GET'])
def addschedules():
    if request.method == 'POST':
        params = request.get_json();
        print(params)
        return {"status": "success"}
    else:
        return render_template("addSchedule.html")


@app.route("/cartOrderDetails")
def showCartOrders():
    carts = retrive_carts()
    orders = retrive_orders()
    return render_template("cartorder.html", carts=carts, orders=orders)


@app.route("/schedulesForCart")
def schedulesForCart():
    return render_template("schedulesForCart.html")


@app.route("/addOrder", methods=['POST', 'GET'])
def addOrder():
    if request.method == 'POST':
        params = request.get_json();
        add_to_cart(params)
        return {"status": "success"}
    else:
        return render_template("addOrder.html")


@app.route("/moveToOrder", methods=['POST'])
def moveToOrderList():
    params = request.get_json();
    move_to_order(params);
    return {"status": "success"}

@app.route("/addScheduleToDB", methods=['POST'])
def addSchTypeInDB():
    params = request.get_json();
    print(params)


# DBHelper functions

def move_to_order(params):
    respJson = {};
    db = get_db()
    curr_time = datetime.datetime.now()
    queryResp = db.execute(SELECT_CARTS + " where id=" + params['id'])
    result = queryResp.fetchall()
    for cart in result:
        cursor = db.execute("insert into OrderDetails(customerName,itemCount,cxEmail,dateOrdered) values (?,?,?,?)",
                            [cart[0], cart[1], cart[2], curr_time.strftime("%Y-%m-%d %H:%M:%S")])
        print(cursor.lastrowid)
    deleteCart = db.execute("delete from CartDetails where id=" + params['id'])
    db.commit()
    print(deleteCart.lastrowid)
    return respJson;


def add_to_cart(params):
    db = get_db()
    curr_time = datetime.datetime.now()
    cursor = db.execute("insert into CartDetails(customerName,itemCount,cxEmail,dateCreated) values (?,?,?,?)",
                        [params['name'], params['count'], params['name'] + "@hotmail.com",
                         curr_time.strftime("%Y-%m-%d %H:%M:%S")])
    print(cursor.lastrowid)
    db.commit()
    print('insertion done')
    add_job_handler(cursor.lastrowid, curr_time, DUMMY_DATA['cxEmail'])


def retrive_carts():
    db = get_db()
    curs = db.execute(SELECT_CARTS)
    res = curs.fetchall()
    print("fetching carts")
    carts = []
    for cart in res:
        print(cart[0])
        carts.append(cart)
    return carts


def retrive_orders():
    db = get_db()
    curs = db.execute(SELECT_ORDERS)
    res = curs.fetchall()
    print("fetching orders")
    orders = []
    for order in res:
        print(order[0])
        orders.append(order)
    return orders


# JOB functions
def send_mail(email):
    '''The send email function that the scheduler is gonna execute'''
    print("sending email to ", email)


def add_job_sched(job_id, run_datetime, func, email):
    '''creating a single scheduler job'''
    sched.add_job(func, JOB_TYPE, run_date=run_datetime, id=job_id, args=[email])
    print("job scheduled for ", email)


def delete_all_jobs_with_id(order_id):
    '''delete all the jobs associated with an order_id, by comparing the jobs_id starting with order_id'''
    for job in sched.get_jobs():
        if (str(job.id)).startswith(str(order_id)):
            sched.remove_job(str(job.id))
            print("deleted job with id :", (job.id))


def add_job_handler(order_id, curr_time, email):
    job_time = curr_time + datetime.timedelta(0, 30)
    # thirty seconds after adding,
    print(job_time)
    job_id = str(order_id) + "_" + job_time.strftime("%Y-%m-%d_%H:%M:%S")
    print(job_id)
    add_job_sched(job_id=job_id, run_datetime=job_time, func=send_mail, email=email)
    return "added "


if __name__ == "__main__":
    app.run(debug=True, port=9090)
