from flask import Flask        
from flask import render_template 
from flask import request
from flask import session
from flask import url_for
from flask import redirect
from flask import make_response
from flask_mysqldb import MySQL

from datetime import datetime

app = Flask(__name__)

app.config['MYSQL_HOST']     = 'localhost'
app.config['MYSQL_USER']     = 'root'
app.config['MYSQL_PASSWORD'] = 'toor'
app.config['MYSQL_DB']       = 'componentlayer_db'

mysql = MySQL(app)


app.secret_key = "test-key"


# --------------------- SQL functions ------------------
def fetch_query(row, table, whereCat, where):
    try:
        if where != '':
            cursor = mysql.connection.cursor()
            cursor.execute(f''' SELECT {row} FROM {table} WHERE {whereCat} = "{where}"''')
        else:
            cursor = mysql.connection.cursor()
            cursor.execute(f''' SELECT {row} FROM {table}''')
        
        data = cursor.fetchall()

        returnData = []
        for item in data:
            returnData.append(item)

        cursor.close()

        return returnData

    except Exception as e:
        print(f"fetch_query: {e}")

def fetch_update_query(cat_sel, selectedCategory):
    try:
        if cat_sel == 1:
            cursor = mysql.connection.cursor()
            
            query = """
                SELECT 
                    c.componentID,
                    c.componentName, 
                    c.componentAmount, 
                    cat.componentCategory,
                    p.componentPackage
                FROM components c
                JOIN categories cat ON c.categoryID = cat.categoryID
                JOIN packages p ON c.packageID = p.packageID
            """
            cursor.execute(query)

        data = cursor.fetchall()
        cursor.close()
        return data


        
    except Exception as e:
        print(f"fetch_update_query: {e}")


#Gets component categories for dropdown menu
def fetch_register_query(): 
    try:
        cursor = mysql.connection.cursor()

        query = """
            SELECT componentCategory FROM categories
        """        
        cursor.execute(query)

        data = cursor.fetchall()

        returnData = []
        for item in data:
            returnData.append(item[0])

        cursor.close()
        return returnData

    except Exception as e:
        print(f"fetch_query: {e}")

def fetch_component_categories(): 
    try:
        cursor = mysql.connection.cursor()

        query = """
            SELECT DISTINCT componentCategory FROM categories
        """        
        cursor.execute(query)

        data = cursor.fetchall()

        returnData = []
        for item in data:
            returnData.append(item[0])

        cursor.close()
        return returnData

    except Exception as e:
        print(f"fetch_categories: {e}")

def fetch_component_amount(compID):
    try:
        cursor = mysql.connection.cursor()

        query = """
            SELECT components.componentAmount FROM components WHERE componentID = %s
        """        
        cursor.execute(query,(compID,))

        data = cursor.fetchone()

        cursor.close()
        return data[0]

    except Exception as e:
        print(f"fetch_amount: {e}")

def fetch_home_query(orderBy, method, category):
    try:
        cursor = mysql.connection.cursor()

        if method == 'POST':
            if orderBy:

                query = """
                    SELECT 
                        c.componentName, 
                        c.componentAmount, 
                        cat.componentCategory,
                        p.componentPackage
                    FROM components c
                    JOIN categories cat ON c.categoryID = cat.categoryID
                    LEFT JOIN packages p ON c.packageID = p.packageID
                    WHERE cat.componentCategory = %s OR %s = "ALL"
                    ORDER BY c.componentAmount ASC
                """
                cursor.execute(query,(category,category,))

            else:
                query = """
                    SELECT 
                        c.componentName, 
                        c.componentAmount, 
                        cat.componentCategory,
                        p.componentPackage
                    FROM components c
                    JOIN categories cat ON c.categoryID = cat.categoryID
                    LEFT JOIN packages p ON c.packageID = p.packageID
                    WHERE cat.componentCategory = %s OR %s = "ALL"
                    ORDER BY c.componentAmount DESC
                """
                cursor.execute(query,(category,category,))
        
        else:
            query = """
                SELECT 
                    c.componentName, 
                    c.componentAmount, 
                    cat.componentCategory,
                    p.componentPackage
                FROM components c
                JOIN categories cat ON c.categoryID = cat.categoryID
                LEFT JOIN packages p ON c.packageID = p.packageID
            """
            cursor.execute(query)

        data = cursor.fetchall()
        cursor.close()
        return data

    except Exception as e:
        print(f"fetch_home_query: {e}")



def fetch_password(row, table, workerID):
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(f''' SELECT {row} FROM {table} WHERE workerID = {workerID} ''')
        dbPass = cursor.fetchone()
        cursor.close()

    except Exception as e:
        print(f"fetch_password: {e}")

    return dbPass


def insert_register_query(componentName, componentPackage, componentCategory, componentAmount):
    try:
        cursor = mysql.connection.cursor()
        new_component_id = 0

        #Test for permission higher than 0
        workerID = request.cookies.get('userID')
        cursor.execute('''SELECT users.workerPermissions FROM users WHERE workerID = %s''', (workerID,))
        permission = cursor.fetchone()
        if permission[0] != 0:
            # Get category ID or create new category
            cursor.execute('''SELECT categoryID FROM categories WHERE componentCategory = %s''', (componentCategory,))
            category_result = cursor.fetchone()

            if category_result:
                categoryID = category_result[0]
            else:
                cursor.execute('''INSERT INTO categories (componentCategory) VALUES (%s)''', (componentCategory,))
                categoryID = cursor.lastrowid


            # Get package ID or create new package type
            cursor.execute('''SELECT packageID FROM packages WHERE componentPackage = %s''', (componentPackage,))
            package_result = cursor.fetchone()

            if package_result:
                packageID = package_result[0]
            else:
                cursor.execute('''INSERT INTO packages (componentPackage) VALUES (%s)''', (componentPackage,))
                packageID = cursor.lastrowid


            cursor.execute('''INSERT INTO components (componentName, componentAmount, packageID, categoryID) VALUES (%s, %s, %s, %s)''', (componentName, componentAmount, packageID, categoryID))
            new_component_id = cursor.lastrowid
            mysql.connection.commit()

        cursor.close()
        return new_component_id

    except Exception as e:
        print(f"insert_register_query: {e}")


def insert_transaction_query(workerID, comp_id, transactionAmount):
    try:
        cursor = mysql.connection.cursor()
        transactionTime = datetime.now().replace(microsecond=0)
        cursor.execute(''' INSERT INTO transactions (workerID, transactionTime, componentID, transactionAmount) VALUES (%s, %s, %s, %s)''', (workerID, transactionTime, comp_id, transactionAmount))
        mysql.connection.commit()
        cursor.close()

    except Exception as e:
        print(f"insert_transaction_query: {e}")


def update_database(comp_id, comp_name, comp_pack, comp_select, comp_amount):
    try:
        cursor = mysql.connection.cursor()

        #Test for permission higher than 0
        workerID = request.cookies.get('userID')
        cursor.execute('''SELECT users.workerPermissions FROM users WHERE workerID = %s''', (workerID,))
        permission = cursor.fetchone()

        if permission[0] != 0:
            cursor.execute('''SELECT packageID FROM packages WHERE componentPackage = %s''', (comp_pack,))
            package_result = cursor.fetchone()

            packID = package_result[0]

            cursor.execute('''SELECT categoryID FROM categories WHERE componentCategory = %s''', (comp_select,))
            category_result = cursor.fetchone()

            catID = category_result[0]

            query = f"""
                UPDATE components
                SET componentName = '{comp_name}', componentAmount = {comp_amount}, packageID = {packID}, categoryID = {catID}
                WHERE componentID = {comp_id};
            """
        else:
            query = f"""
                UPDATE components
                SET componentAmount = {comp_amount}
                WHERE componentID = {comp_id}
            """

        cursor.execute(query)
        mysql.connection.commit()
        cursor.close()

    except Exception as e:
        print(f"update_database: {e}")

# --------------------------- Log page ---------------------------

@app.route("/log", methods=['GET', 'POST'])
def log():   
    if not 'user' in session:
        return redirect(url_for('login'))
    
    data = fetch_query("*", "transactions", '', '')

    return render_template('log.html', data=data)



# ---------------------- Update component page -------------------
@app.route("/update_component", methods=['GET', 'POST'])
def update_component():
    if not 'user' in session:
        return redirect(url_for('login'))
    
    arg = ""
    data = []
    if request.method == "GET":
        if str(request.args.get('comp')) != 'None':
            arg = str(request.args.get('comp'))
            data = fetch_update_query(1, arg)

            selectorData = fetch_component_categories()
        else:
            selectorData = fetch_component_categories()
            data.append("No_print")
        
    if request.method == "POST":
        comp_id     = str(request.form.get('comp_id'))
        comp_name   = str(request.form.get('component_name'))
        comp_pack   = str(request.form.get('component_package'))
        comp_select = str(request.form.get('component_selector'))
        comp_amount = str(request.form.get('component_amount'))

        current_comp_amount = fetch_component_amount(comp_id)
        update_database(comp_id, comp_name, comp_pack, comp_select, comp_amount)

        workerID = request.cookies.get('userID')
        insert_transaction_query(workerID, comp_id, str(int(comp_amount)-current_comp_amount))

        if str(request.args.get('comp')) != 'None':
            arg = str(request.args.get('comp'))
            data = fetch_update_query(1, arg)

            selectorData = fetch_component_categories()
        else:
            selectorData = fetch_component_categories()
            data.append("No_print")


    return render_template('update_component.html', data=data, selectorData=selectorData, arg=arg)



# --------------------- Register component page ------------------
@app.route("/register_component", methods=['GET', 'POST'])
def register_component():
    if not 'user' in session:
        return redirect(url_for('login'))
    
    data = fetch_register_query()

    if request.method == "POST":
        comp_name   = str(request.form.get('component_name'))
        comp_pack   = str(request.form.get('component_package'))
        comp_select = request.form.get('component_selector')
        comp_cat    = request.form.get('component_category')
        comp_amount = request.form.get('component_amount')

        try:
            if comp_select == "none":
                if comp_cat == "":
                    status_msg = "No category selected or entered!"
                    return render_template('register_component.html', status_msg=status_msg)
                
                new_comp_id = insert_register_query(comp_name, comp_pack, comp_cat, comp_amount)
                if not new_comp_id:
                    status_msg = "You don't have permission for this action!"
                    return render_template('register_component.html', status_msg=status_msg)

                workerID = request.cookies.get('userID')
                insert_transaction_query(workerID, new_comp_id, comp_amount)

                status_msg = "Component has been registered"
                return render_template('register_component.html', status_msg=status_msg)
            
            else:
                new_comp_id = insert_register_query(comp_name, comp_pack, comp_select, comp_amount)
                if not new_comp_id:
                    status_msg = "You don't have permission for this action!"
                    return render_template('register_component.html', status_msg=status_msg)
                
                workerID = request.cookies.get('userID')
                insert_transaction_query(workerID, new_comp_id, comp_amount)

                status_msg = "Component has been registered"
                return render_template('register_component.html', status_msg=status_msg)

        except Exception as e:
            print(e)
            status_msg = "Something went wrong!"
            return render_template('register_component.html', status_msg=status_msg)
    
    
    return render_template('register_component.html', data=data)



# --------------------------- Main page ---------------------------
@app.route("/", methods=['GET', 'POST'])
def home():    
    categories = fetch_component_categories()
    categories.insert(0,"All")

    if not 'user' in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        selected_sort  = request.form.get('select_sort')
        selected_value = request.form.get('select_category')

        if selected_sort == "select_asc":
            data = fetch_home_query(True, 'POST', selected_value)
        else:
            data = fetch_home_query(False, 'POST', selected_value)
        
        return render_template("index.html", data=data, categories=categories, selected_value=selected_value, order_select=selected_sort, selected_cat=selected_value)
    
    else:
        data = fetch_home_query(True, 'GET', "ALL")
        return render_template("index.html", data=data, categories=categories, selected_value="All",order_select="select_asc",selected_cat="All")
        
    

# -------------------------- Login page --------------------------
@app.route('/set_cookie')
def set_cookie():
    userID = request.args.get('userID')
    resp = make_response(redirect(url_for('home')))  
    resp.set_cookie('userID', userID, max_age=60*60*24, httponly=False, secure=False, samesite="Lax")  # Expires in 1 day
    return resp


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        workerID = request.form['workerID']
        password = request.form['password']

        try:
            dbPass = fetch_password('workerPassword', 'users', workerID)
            
            if password == dbPass[0]:
                session['user'] = workerID
                session.modified = True
                return redirect(url_for('set_cookie', userID=workerID))
            
            else:
                err_msg = "Wrong password or Worker ID!"
                return render_template('login.html', err_msg=err_msg)
            
        except Exception as e:
                err_msg = "Wrong password or Worker ID!"
                return render_template('login.html', err_msg=err_msg)

    return render_template('login.html')



# -------------------------- Logout page --------------------------
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.clear()
    session.modified = True

    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)