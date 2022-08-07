from flask import Flask, g
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from database import get_db

app = Flask(__name__)
sched = BackgroundScheduler(daemon=True)
sched.start()
JOB_TYPE = 'date'
SELECT_ORDERS = "select * from OrderDetails"
SELECT_CARTS = "select * from CartDetails"
SELECT_SCHEDULES = "select * from ScheduleTemplate"


@app.teardown_appcontext
def close_db(error):
    '''when the flask app stops, the db is closed'''
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


def send_mail():
    '''The send email function that the scheduler is gonna execute'''
    print("sending hello mails ")


def add_job(job_id, run_datetime, func):
    '''creating a single scheduler job'''
    sched.add_job(func, JOB_TYPE, run_date=run_datetime, id=job_id)


def delete_all_jobs_with_id(order_id):
    '''delete all the jobs associated with an order_id, by comparing the jobs_id starting with order_id'''
    for job in sched.get_jobs():
        if (str(job.id)).startswith(str(order_id)):
            sched.remove_job(str(job.id))
            print("deleted job with id :", (job.id))


@app.route('/')
def index():
    for i in (sched.get_jobs()):
        print(i)
    return "jobs listmo"


@app.route('/add/<int:order_id>')
def add(order_id):
    curr_time = datetime.datetime.now()
    job_time = curr_time + datetime.timedelta(0, 30)
    print(job_time)
    job_id = str(order_id) + "_" + job_time.strftime("%Y-%m-%d_%H:%M:%S")
    print(job_id)
    add_job(job_id=job_id, run_datetime=job_time, func=send_mail)
    return "added "


@app.route('/remove/<int:order_id>')
def remove(order_id):
    delete_all_jobs_with_id(order_id)
    return "remove "


@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    pass


@app.route('/add-to-order', methods=['POST'])
def add_to_order():
    pass


@app.route('/view-carts', methods=['GET'])
def view_carts():
    db = get_db()
    cur = db.execute(SELECT_CARTS)
    res = cur.fetchall()
    str = ""
    for r in res:
        str = str + str(r)
    return str


@app.route('/view-orders', methods=['GET'])
def view_orders():
    db = get_db()
    cur = db.execute(SELECT_ORDERS)
    res = cur.fetchall()
    str = ""
    for r in res:
        str = str + str(r)
    return str


if __name__ == "__main__":
    app.run(debug=True)



