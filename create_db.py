import sqlite3

create_schedule = '''
create table if not exists SchedulesTemplate (
    id integer primary key autoincrement,
    templateName text not null,
    schDetails text not null,
    isDefault boolean not null,
    dateCreated datetime not null
);
 '''

create_cart = '''
create table if not exists CartDetails (
    id integer primary key autoincrement,
    customerName text not null,
    itemCount text not null,
    cxEmail text not null,
    dateCreated datetime not null
);
'''

create_order = '''
create table if not exists OrderDetails (
    id integer primary key autoincrement,
    customerName text not null,
    itemCount text not null,
    cxEmail text not null,
    dateOrdered datetime not null
);
'''

con = sqlite3.connect("abandon.db")

con.execute(create_schedule)
con.execute(create_cart)
con.execute(create_order)

con.close()
