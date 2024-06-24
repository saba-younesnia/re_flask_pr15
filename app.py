from flask import *
import sqlite3

app = Flask(__name__)

app.config['DATABASE']='db1.db'
def connect_to_db():
    db=getattr(g,'_database',None)
    if db is None:
        db=g._database=sqlite3.connect(app.config['DATABASE'])
    return db

@app.route('/',methods=['GET','POST'])
def index():
    db = connect_to_db()
    cursor = db.cursor()
    if request.method == 'POST':
        cursor.execute("select employees.name, employees.family , sum(salaries.salary) from employees inner join salaries on employees.id=salaries.id group by employees.name, employees.family")
        data = cursor.fetchall()
        cursor.execute("select employees.*, sum(salaries.salary) as total_salary from employees inner join salaries on employees.id=salaries.id group by employees.id having total_salary=(select max(total_salary) from (select sum(salary) as total_salary from salaries group by id ))")
        data1=cursor.fetchall()
        return render_template('index.html',data=data,data1=data1)
    else:
        cursor.execute("select employees.name, employees.family , sum(salaries.salary) from employees inner join salaries on employees.id=salaries.id group by employees.name, employees.family")
        data=cursor.fetchall()
        return render_template('index.html',data=data)

if __name__ == '__main__':
    app.run()
