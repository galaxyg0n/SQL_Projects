from flask import Flask        
from flask import render_template 
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB']       = 'ComponentLayer_schema'

mysql = MySQL(app)


app.secret_key = "test-key"


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        workerID = request.form['workerID']
        password = request.form['password']

        try:
            cursor = mysql.connection.cursor()
            cursor.execute(''' SELECT workerPassword FROM users WHERE workerID = %s ''', (workerID))
            dbPass = cursor.fetchone()

            print(dbPass)

            if password == dbPass[0]:
                session['user'] = workerID
                session.modified = True
                return redirect(url_for('home'))
            
            else:
                err_msg = "Wrong password or Worker ID!"
                return render_template('login.html', err_msg=err_msg)
            
        except Exception as e:
                err_msg = "Wrong password or Worker ID!"
                return render_template('login.html', err_msg=err_msg)
        
        finally:
            cursor.close()

    return render_template('login.html')


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    session.modified = True

    return redirect(url_for('home'))



@app.route("/", methods=['GET', 'POST'])
def home():
    if not 'user' in session:
        return redirect(url_for('login'))

    cursor = mysql.connection.cursor()
    cursor.execute(''' SELECT componentName, componentDescription, componentCategory, componentAmount FROM components ''')
    data = cursor.fetchall()
    cursor.close()

    if request.method == 'POST':
        selected_value = request.form.get('select')
        return render_template("index.html", data=data, selected_value=selected_value)
    else:
        return render_template("index.html", data=data)
        
    

if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)