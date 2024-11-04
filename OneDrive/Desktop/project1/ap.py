# from flask import Flask, request, redirect, url_for, flash, render_template
# import sqlite3

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'  # Change this to a secure key for production

# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
#     if request.method == 'POST':
#         username = request.form['username'].strip()  # Remove whitespace
#         password = request.form['password'].strip()
        
#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()
        
#         # Check if username and password match an entry in the admin table
#         cursor.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password))
#         user = cursor.fetchone()
#         conn.close()  # Always close the connection after finishing

#         if user:
#             # If user exists, log in successfully
#             flash('Login successful!')
#             return redirect(url_for('dashboard'))  # Redirect to dashboard route
#         else:
#             flash('Invalid username or password.')

#     return render_template('admin.html')  # Render your login template

# @app.route('/dashboard')
# def dashboard():
#     # Here you would typically fetch dashboard data
#     return render_template('dashboard.html', username='Admin')  # Pass username or any necessary data

# if __name__ == '__main__':
#     app.run(debug=True)
# @app.route('/admin', methods=['GET', 'POST'])
# def admin():
#     if request.method == 'POST':
#         username = request.form['username']  # Remove the extra space
#         password = request.form['password']
        
#         conn = sqlite3.connect('database.db')
#         cursor = conn.cursor()
        
#         # Check if username and password match an entry in the admin table
#         cursor.execute('SELECT * FROM admin WHERE username = ? AND password = ?', (username, password))
#         user = cursor.fetchone()
#         conn.close()  # Always close the connection after finishing

#         if user:
#             # If user exists, log in successfully
#             flash('Login successful!')
#             return redirect(url_for('dashboard'))  # Make sure to define ahome route
#         else:
#             flash('Invalid username or password.')

#     return render_template('admin.html')
# @app.route('/dashboard')
# def dashboard():
#     # Here you would typically fetch dashboard data
#     username = session.get('username')
#     return render_template('dashboard.html', username=username)
#       # Pass username or any necessary data
