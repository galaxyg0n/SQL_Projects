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
def fetch_update_query(cat_sel):
    try:
        if cat_sel == 1:
            cursor = mysql.connection.cursor()
            cursor.execute(''' SELECT * FROM components WHERE  ''')

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
        print(f"fetch_query: {e}")

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
                    JOIN packages p ON c.packageID = p.packageID
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
                    JOIN packages p ON c.packageID = p.packageID
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
                JOIN packages p ON c.packageID = p.packageID
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
    """
    Description:
        Function to insert data in the register table \n
    
    Args:
        componentName: Name of the component
        componentDescription: Description of the component
        componentCategory: Category of the component (selected from html selector or typed if it didn't excist)
        componentAmount: Amount of the inserted component
    
    Returns:
        Nothing
    """
    try:
        cursor = mysql.connection.cursor()

        # Get category ID or create new category
        cursor.execute('''SELECT categoryID FROM categories WHERE componentCategory = %s''', (componentCategory,))
        category_result = cursor.fetchone()
        print(f"Category result: {category_result[0]}")

        if category_result:
            categoryID = category_result[0]
        else:
            cursor.execute('''INSERT INTO categories (componentCategory) VALUES (%s)''', (componentCategory,))
            categoryID = cursor.lastrowid


        # Get package ID or create new package type
        cursor.execute('''SELECT packageID FROM packages WHERE componentPackage = %s''', (componentPackage,))
        package_result = cursor.fetchone()
        print(f"Package result: {package_result[0]}")

        if package_result:
            packageID = package_result[0]
        else:
            cursor.execute('''INSERT INTO packages (componentPackage) VALUES (%s)''', (componentPackage,))
            packageID = cursor.lastrowid


        cursor.execute('''INSERT INTO components (componentName, componentAmount, packageID, categoryID) VALUES (%s, %s, %s, %s)''', (componentName, componentAmount, packageID, categoryID))

        mysql.connection.commit()
        cursor.close()

    except Exception as e:
        print(f"insert_register_query: {e}")


def insert_transaction_query(workerID, transactionTime, componentName, transactionAmount):
    """
    Description:
        Function to insert data in the transaction table \n
    
    Args:
        workerID: Worker ID
        transactionTime: Time of transaction fetched from datetime.now()
        componentName: Name of component
        transactionAmount: Amount of the inserted component
    
    Returns:
        Nothing
    """
    try:
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO transactions (workerID, transactionTime, componentName, transactionAmount) VALUES (%s, %s, %s, %s)''', (workerID, transactionTime, componentName, transactionAmount))
        mysql.connection.commit()
        cursor.close()

    except Exception as e:
        print(f"insert_transaction_query: {e}")



# --------------------------- Log page ---------------------------

@app.route("/log", methods=['GET', 'POST'])
def log():
    """
    Description:
        Handler function for log page
    
    Args:
        HTML methods (GET and POST)
    
    Returns:
        Renders log.html
    """
        
    if not 'user' in session:
        return redirect(url_for('login'))
    
    cursor = mysql.connection.cursor()

    query = """
            SELECT * FROM transactions
        """        
    cursor.execute(query)

    data = cursor.fetchall()

    returnData = []
    for item in data:
        returnData.append(item)
    print(returnData)
    cursor.close()
        
    return render_template('log.html', data=returnData)



# ---------------------- Update component page -------------------
@app.route("/update_component", methods=['GET', 'POST'])
def update_component():
    """
    Description:
        Handler function for update component page \n
        - Checks if a category has been selected and updates the page with a GET request using url queries
        
        - Updates database table according to the inserted data in the html form
    
    Args:
        HTML methods (GET and POST)
    
    Returns:
        Renders update_component.html
    """

    if not 'user' in session:
        return redirect(url_for('login'))
    
    data = []
    if request.method == "GET":

        if str(request.args.get('comp')) != 'None':
            arg = str(request.args.get('comp'))
            data = fetch_update_query(1, arg)

            selectorData = fetch_query('*', 'components', '', '')
            
        else:
            selectorData = fetch_query('*', 'components', '', '')
            data.append("No_print")

    return render_template('update_component.html', data=data, selectorData=selectorData)



# --------------------- Register component page ------------------
@app.route("/register_component", methods=['GET', 'POST'])
def register_component():
    """
    Description:
        Handler function for register component page \n
        - Gets all relevant data from the html form and inserts in the database using insert_register_query()

        - Adds transaction "event" to the database using insert_transaction_query()
    
        - Gets the time of the transaction automatically using the datetime library
    
    Args:
        HTML methods (GET and POST)
    
    Returns:
        Renders register_component.html
    """

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
                
                insert_register_query(comp_name, comp_pack, comp_cat, comp_amount)

                workerID = request.cookies.get('userID')
                now = datetime.now().replace(microsecond=0)
                insert_transaction_query(workerID, now, comp_name, comp_amount)

                status_msg = "Component has been registered"
                return render_template('register_component.html', status_msg=status_msg)
            
            else:
                insert_register_query(comp_name, comp_pack, comp_select, comp_amount)
                
                workerID = request.cookies.get('userID')
                now = datetime.now().replace(microsecond=0)
                insert_transaction_query(workerID, now, comp_name, comp_amount)

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
    """
    Handler function for update component page \n
    - Checks if a category has been selected and updates the page with a GET request using url queries
    
    - Updates database table according to the inserted data in the html form
    
    Args:
        HTML methods (GET and POST)
    
    Returns:
        Renders update_component.html
    """
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
    """
    Description:
        Sets userID cookie to the logged in workerID
    
    Args:
        Nothing
    
    Returns:
        make_response response (html status response)
    """
    userID = request.args.get('userID')
    print(userID)
    resp = make_response(redirect(url_for('home')))  
    resp.set_cookie('userID', userID, max_age=60*60*24, httponly=False, secure=False, samesite="Lax")  # Expires in 1 day
    return resp


@app.route("/login", methods=['GET', 'POST'])
def login():
    """
    Description:
        Handler function for the login page \n
        - Gets the html form data
        - Fetches password from corresponding workerID in the users database
        - Checks if the typed password matches the fetched password

    
    Args:
        HTML methods (GET and POST)
    
    Returns:
        Renders the login.html page
    """
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
    """
    Description:
        Handler function for logging out \n
        - Clears the session
    
    Args:
        HTML methods (GET and POST)
    
    Returns:
        Redirects to home page which will redirect to login automatically
    """
    session.clear()
    session.modified = True

    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8000, debug=True)