from flask import Flask, render_template, request, redirect, url_for, session, flash
import random
import re
import sqlite3
import smtplib
import hashlib
# from urllib.parse import urlencode
from flask_mail import Mail


app = Flask(__name__)
app.secret_key = '123456789'
conn = sqlite3.connect('database.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                  (id INTEGER PRIMARY KEY, 
                   username TEXT UNIQUE, 
                   email TEXT UNIQUE, 
                   age INTEGER, 
                   gender TEXT, 
                   phone TEXT UNIQUE, 
                   password TEXT)''')
cursor.execute('''CREATE TABLE IF NOT EXISTS admin
                  (username TEXT UNIQUE,password TEXT UNIQUE,email TEXT UNIQUE )''')   
conn.execute("""
        CREATE TABLE IF NOT EXISTS user_order (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            user_name TEXT, 
            food_name TEXT, 
            food_quantity INTEGER, 
            food_price REAL,
            status TEXT DEFAULT 'Processing'
        )
    """)
conn.execute('''
        CREATE TABLE IF NOT EXISTS orders(
            order_id INTEGER, 
            user_name TEXT, 
            food_name TEXT, 
            food_price REAL,
            status TEXT 
        )
    ''')
conn.execute(''' create table if not exists fav(
        user_name text,
        food_name text unique,
        food_price float,
        rating float)''')
              
conn.commit()
conn.close()

# Mail configuration
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = 'patasaubalu80@gmail.com'  # Update with your email
app.config['MAIL_PASSWORD'] = 'xsdd binm jomp cwzb'   # Update with your email password
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
mail = Mail(app)


    

def send_otp(email, otp):
    subject = "Your OTP Code"
    body = f"Your OTP is {otp}."
    message = f"Subject: {subject}\n\n{body}"
    
    with smtplib.SMTP(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]) as server:
        server.starttls()
        server.login(app.config["MAIL_USERNAME"], app.config['MAIL_PASSWORD'])
        server.sendmail(app.config["MAIL_USERNAME"], email, message)




# @app.route('/')
# def dash11():
#     return render_template('dashboard.html')



@app.route('/biryani')
def biryani():
    return render_template('house.html')

@app.route('/hotel')
def hotel():
    return render_template('aachi.html')

@app.route('/burger')
def burger():
    return render_template('burger.html')
@app.route('/cakes')
def cakes():
    return render_template('house.html')

@app.route('/kfc')
def kfc():
    return render_template('kfc.html')

@app.route('/pizza')
def pizza():
    return render_template('pizza.html')
@app.route('/saravana')
def saravana():
    return render_template('saravana.html')

@app.route('/uniq')
def uniq():
    return render_template('uniq.html')




@app.route('/')
def home():
    return render_template('home.html')
@app.route('/about')
def about():
    return render_template('about.html')
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        age = int(request.form['age'])
        gender = request.form['gender']
        phone = request.form['phone']

        # Validate password
        if not re.match(r'^(?=.*[0-9])(?=.*[!@#$%^&*])(?=.{8,})', password):
            flash('Password must be at least 8 characters long, contain 1 number, and 1 special character.')
            return redirect(url_for('signin'))

        # Validate email
        if not re.match(r'^\S+@\S+\.\S+$', email):
            flash('Invalid email format.')
            return redirect(url_for('signin'))

        # Validate age
        if age > 100:
            flash('Age must be less than 100.')
            return redirect(url_for('signin'))

        # Check for existing username, email, and phone
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            flash('Username already exists.')
            conn.close()
            return redirect(url_for('signin'))

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            flash('Email already exists.')
            conn.close()
            return redirect(url_for('signin'))

        cursor.execute("SELECT * FROM users WHERE phone = ?", (phone,))
        if cursor.fetchone():
            flash('Phone number already exists.')
            conn.close()
            return redirect(url_for('signin'))

        conn.close()

        # Send OTP
        otp = random.randrange(100000, 999999)
        send_otp(email, otp)

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        session['otp'] = otp
        session['user_data'] = {
            'username': username,
            'email': email,
            'password': password_hash,
            'age': age,
            'gender': gender,
            'phone': phone
        }

        return redirect(url_for('verify_otp'))

    return render_template('signin.html')
@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        user_otp = int(request.form['otp'])
        if user_otp == session.get('otp'):
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            user_data = session.get('user_data')
            cursor.execute('INSERT INTO users (username, email, password, age, gender, phone) VALUES (?, ?, ?, ?, ?, ?)',
                           (user_data['username'], user_data['email'], user_data['password'], user_data['age'], user_data['gender'], user_data['phone']))
            conn.commit()
            conn.close()

            flash("Register successful")
            session.pop('otp', None)  # Clear OTP
            session.pop('user_data', None)  # Clear user data
            return redirect(url_for("home"))
            
        else:
            flash('Invalid OTP. Please try again.')
            return redirect(url_for('verify_otp'))

    return render_template('verify_otp.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form['identifier']  # username or phone number
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE username = ? OR phone = ?', (identifier, identifier))
        user = cursor.fetchone()
        
        if user:
            stored_password = user[6]  # Assuming password is stored in the 6th index
            if stored_password == hashlib.sha256(password.encode()).hexdigest():
                session['username'] = user[1]  # Assuming username is at index 1
                flash('Login successful!')
                return redirect('/userdashboard')
            else:
                flash('Incorrect password. Did you forget your password?')
                return redirect(url_for('login'))
        else:
            flash('Invalid username or phone number.')
            return redirect(url_for('login'))

    return render_template('login.html')
@app.route('/userdashboard')
def dash():
    if 'username' in session:
        user = session['username']
        return render_template('dashboard.html', name=user)
    else:
        flash('You need to log in first.')
        return redirect(url_for('login'))
@app.route('/add/<n>/<a>', methods=["GET", "POST"])
def add(n, a):
    user = session['username']
    if request.method == "POST":
       
        fname = n
        price = int(a)
        quantity = int(request.form['item'])

        conn = sqlite3.connect('database.db')
        cur = conn.cursor()

        cur.execute('SELECT food_quantity FROM user_order WHERE user_name=? AND food_name=? AND status=?', (user, fname, 'Processing'))
        data = cur.fetchone()

        if data:
            new_quantity = data[0] + quantity
            conn.execute('UPDATE user_order SET food_quantity=? WHERE user_name=? AND food_name=?', (new_quantity, user, fname))
        else:
            conn.execute('INSERT INTO user_order (user_name, food_name, food_quantity, food_price) VALUES (?, ?, ?, ?)', (user, fname, quantity, price*quantity*10))

        conn.commit()
        return redirect(url_for('cart'))

    return render_template('dashboard.html', name=user)


@app.route('/cart')
def cart():
    user = session['username']
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_order WHERE user_name=?", (user,))
    orders = cur.fetchall()

    conn.close()
    return render_template('cart.html', name=user, order=orders)    

@app.route('/myorders')
def myorders():
    user = session.get('username')  # Use get() to avoid KeyError
    if not user:
        return "User not logged in", 403  # Return an error if the user is not logged in

    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Enable named access to rows
    cur = conn.cursor()

    # Fetch orders for the logged-in user
    cur.execute('SELECT * FROM orders WHERE user_name=? order by status desc  ', (user, ))
    data = cur.fetchall()

    conn.close()  # Close the connection
    return render_template('order.html', d=data)

@app.route('/buy')
def buy():
    user = session['username']
    if not user:
            return "User not logged in", 403  
       
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    cur = conn.cursor()

        
    cur.execute("SELECT * FROM user_order WHERE user_name=? AND status=?", (user, 'Processing'))
    orders1 = cur.fetchall()

      
    for order in orders1:
            conn.execute('INSERT INTO orders (order_id, user_name, food_name, food_price, status) VALUES (?, ?, ?, ?, ?)', 
                        (order['order_id'], order['user_name'], order['food_name'], order['food_price'], order['status']))


    cur.execute("delete from user_order WHERE user_name=? AND status=?", (user, 'Processing'))
    conn.commit()
    conn.close()
    flash('ORDER PLACED SUCCESSFULLY')
    return redirect(url_for('myorders'))
@app.route('/buy1')
def buy1():
    return render_template('buy.html')
@app.route('/update/<int:order_id>')
def update(order_id):

    order_id1=order_id
    conn =sqlite3.connect('database.db')
    cur = conn.cursor()
    conn.execute('update  orders set status=? where order_id=?',("Completed",order_id1))
    conn.commit()
    return redirect(url_for('currentorder'))


@app.route('/fav/<n>/<a>/<r>', methods=['POST', 'GET'])
def fav(n, a, r):
        user = session['username']  
   

        food_name = n
        price = float(a)
        rating = float(r)

       
        conn =sqlite3.connect('database.db')
        cur = conn.cursor()

       
        cur.execute('SELECT * FROM fav WHERE user_name=? AND food_name=?', (user, food_name))
        data = cur.fetchone()

       
        if data is None:
            cur.execute('INSERT INTO fav (user_name, food_name, food_price, rating) VALUES (?, ?, ?, ?)', 
                        (user, food_name, price, rating))
            conn.commit()
            return redirect(url_for('favorite'))

       
       



@app.route('/favorite')
def favorite():
    user = session['username'] 
    conn =sqlite3.connect('database.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM fav WHERE user_name=?', (user))
    fav_data = cur.fetchall()

       
    conn.close()

    return render_template('favourite.html', d=fav_data)

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()

        if user:
            # Generate and send OTP to the user's email
            otp = random.randrange(100000, 999999)
            send_otp(email, otp)

            session['otp'] = otp
            session['email'] = email

            flash('OTP has been sent to your email.')
            return redirect(url_for('reset_password'))
        else:
            flash('Email not found in our system.')
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')

@app.route('/reset-password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'POST':
        user_otp = int(request.form['otp'])
        new_password = request.form['new_password']

        if user_otp == session.get('otp'):
            # Update password in the database
            # (new_password.encode())
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = ? WHERE email = ?', (new_password, session.get('email')))
            conn.commit()
            conn.close()

            flash('Password reset successful! You can now log in with your new password.')
            session.pop('otp', None)  # Clear OTP
            session.pop('email', None)  # Clear email
            return redirect(url_for('login'))
        else:
            flash('Invalid OTP. Please try again.')
            return redirect(url_for('reset_password'))

    return render_template('reset_password.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username'].strip()  # Trim any extra spaces
        password = request.form['password']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Fetch the user by username
        cursor.execute('SELECT * FROM admin WHERE username = ? and password=?', (username,password))
        user = cursor.fetchone()
        conn.close()  # Always close the connection after finishing

        if user and(user[1], password):  # Assuming user[1] is the password
            session['username'] = username  # Store username in session
            flash('Login successful!')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')

    return render_template('admin.html')

@app.route('/dashboard')
def dashboard():
    username = session.get('username')
    if username is None:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('admin'))

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Fetch total user count
    cursor.execute('SELECT COUNT(*) FROM users')
    total_users = cursor.fetchone()[0]
    conn.close()

    return render_template('admindashboard.html', username=username, total_users=total_users)
@app.route('/add_admin', methods=['GET', 'POST'])
def add_admin():
    if request.method == 'POST':
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Check for existing username
        cursor.execute('SELECT * FROM admin WHERE username=?', (username,))
        if cursor.fetchone():
            flash('Username already exists.')
            conn.close()  # Close the connection before redirect
            return redirect(url_for('add_admin'))  # Corrected redirect

        # Check for existing email
        cursor.execute('SELECT * FROM admin WHERE email=?', (email,))
        if cursor.fetchone():
            flash('Email already exists.')
            conn.close()  # Close the connection before redirect
            return redirect(url_for('add_admin'))
        cursor.execute('INSERT INTO admin (username, email, password) VALUES (?, ?, ?)',
                       (username, email, password))
        conn.commit()
        conn.close()
        flash('Admin added successfully!')
        return redirect(url_for('dashboard'))

    return render_template('add_admin.html')
@app.route('/remove_admin', methods=['GET', 'POST'])
def remove_admin():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Get the current admin's username
    current_username = session.get('username')

    if request.method == 'POST':
        # Get the username to be deleted from the form
        username_to_delete = request.form['username']

        # Ensure the logged-in admin cannot delete themselves
        if username_to_delete == current_username:
            flash('You cannot delete your own account.')
        else:
            # Delete the admin from the database
            cursor.execute('DELETE FROM admin WHERE username = ?', (username_to_delete,))
            conn.commit()
            flash(f'Admin {username_to_delete} removed successfully!')

    # Fetch all admins except the current one
    cursor.execute('SELECT username FROM admin WHERE username != ?', (current_username,))
    admins = cursor.fetchall()
    conn.close()

    return render_template('remove_admin.html', admins=admins)
@app.route('/search_customer', methods=['GET', 'POST'])
def search_customer():
    results = []
    if request.method == 'POST':
        search_query = request.form['search_query']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username LIKE ? OR email LIKE ? OR phone LIKE ?", 
                       (f'%{search_query}%', f'%{search_query}%', f'%{search_query}%'))
        results = cursor.fetchall()
        conn.close()

        if not results:
            flash('No data found.')
            return redirect(url_for('dashboard'))
    return render_template('search_customer.html', results=results)
@app.route('/currentorder')
def currentorder():
    # Connect to the SQLite database
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row  # Enable row access by name
    cur = conn.cursor()

    # Query to join users and orders based on the username
    cur.execute( '''
    SELECT 
        users.username,
        users.email,
        users.phone,
        orders.order_id,  -- Assuming 'order_id' is a column in orders
        orders.food_name,  -- Replace with actual column names
        orders.status  -- Replace with actual column names
    FROM 
        users
    JOIN 
        orders ON users.username = orders.user_name
    ORDER BY 
        users.username
    ''')
    
   
    results = cur.fetchall()  # Fetch all results from the query

    conn.close()  # Don't forget to close the connection

    return render_template('currentorder.html', result=results)
@app.route('/update_password', methods=['GET', 'POST'])
def update_password():
    if request.method == 'POST':
        username_or_email = request.form['username_or_email'].strip()
        new_password = request.form['new_password']
        
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Check if the username or email exists
        cursor.execute('SELECT * FROM admin WHERE username = ? OR email = ?', (username_or_email, username_or_email))
        user = cursor.fetchone()

        if user:
            # Update the password
            cursor.execute('UPDATE admin SET password = ? WHERE username = ? OR email = ?', (new_password, username_or_email, username_or_email))
            conn.commit()
            flash('Password updated successfully!')
        else:
            flash('No user found with that username or email.')

        conn.close()
        return redirect(url_for('update_password'))  # Redirect to the same page

    return render_template('update_password.html') 
if __name__ == '__main__':
    app.run(debug=True)


