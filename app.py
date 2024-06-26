from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysupersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mjay0001@localhost/carrental'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    
    
# TODO
# Create models for rental and car tables


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

@app.route('/')
@app.route('/index')
def dashboard():
    # Add logic for the dashboard route
    return render_template('index.html')

@app.errorhandler(404)
def bar(error):
    return render_template('error.html'), 404

@app.route('/admin')
def admin_login():
    return render_template('admin/login.html')

@app.route('/adminlogin', methods=['GET', 'POST'])
def admin_configs():
    if request.method == "post":
        uname = request.form['admin_uname']
        passwd = request.form['adminpasswd']
        
        # TODO
        # validate admin login details against some stored details
        
        
    return render_template('/admin/admin-view.html') 

        
@app.route('/admin/dashboard')
def admin_dashboard():
    # Connect to the database and fetch system statistics
    cur.execute("SELECT COUNT(*) FROM user")
    total_customers = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM car")
    total_cars = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM rental")
    total_rentals = cur.fetchone()[0]
    conn.close()
    return render_template('admin/admin-view.html', total_customers=total_customers, total_cars=total_cars, total_rentals=total_rentals)

@app.route('/contactUs')
def contact():
    return render_template('contact.html')

@app.route('/aboutUs')
def aboutus():
    return render_template('about.html')

@app.route('/booking')
def booking():
    if 'email' in session:
        return render_template('bookingsuccess.html')
    else:
        flash('Kindly login to continue with your booking', 'error')
        return render_template('index.html')

@app.route('/Toyota')
def toyotapage():
    return render_template('toyota/toyota.html')

@app.route('/Toyota/<toyota_brand>')
def toyotabrands(toyota_brand):
    return render_template(f'toyota/{toyota_brand}')

@app.route('/Mazda')
def mazdapage():
    return render_template('mazda/mazda.html')

@app.route('/Mazda/<mazda_brand>')
def mazdabrands(mazda_brand):
    return render_template(f'mazda/{mazda_brand}')

@app.route('/Mercedes')
def mercedespage():
    return render_template('mercedes/mercedes.html')

@app.route('/Mercedes/<mercedes_brand>')
def mercedesbrands(mercedes_brand):
    return render_template(f'mercedes/{mercedes_brand}')

@app.route('/Nissan')
def nissanpage():
    return render_template('nissan/nissan.html')

@app.route('/Nissan/<nissan_brand>')
def nissanbrands(nissan_brand):
    return render_template(f'nissan/{nissan_brand}')

@app.route('/Honda')
def hondapage():
    return render_template('honda/honda.html')

@app.route('/Honda/<honda_brand>')
def hondabrands(honda_brand):
    return render_template(f'honda/{honda_brand}')

if __name__ == '__main__':
    # When running this script directly, create the database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)
    