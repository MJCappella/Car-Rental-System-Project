from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from app import User

app = Flask(__name__)
db = SQLAlchemy(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['firstname']
        last_name = request.form['lastname']
        email= request.form['email']
        password = request.form['password']
        confirm_password = request.form['password2']

        if password != confirm_password:
            flash('Password and Confirm Password do not match. Please try again.', 'error')
        else:
            # TODO
            # Validate login details and hash before storage
            # Hash the password before storing it in the database
            # password_hash = generate_password_hash(password, method='pbkdf2:sha256')

            new_user = User(first_name=first_name, last_name=last_name, email=email, password_hash=password) #replace password with password_hash

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('dashboard'))

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email)

        if user :
            
            # TODO validate details and dehash
        #and check_password_hash(user.password_hash, password): #replace password with password_hash
            # Login successful
            flash('Login successful', 'success')
            session['email'] = email
            return render_template('index.html')
        else:
            # Login failed
            flash('Login failed. Please check your email and password.', 'danger')

    return render_template('index.html')

@app.route('/logout')
def logout():
    session.pop('email', None) 
    flash('You have logged out successfully', 'success')
    return redirect(url_for('dashboard'))
