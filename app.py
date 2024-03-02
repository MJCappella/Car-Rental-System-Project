from flask import Flask, render_template, request, redirect, url_for, flash
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
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username= request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Password and Confirm Password do not match. Please try again.', 'danger')
        else:
            # Hash the password before storing it in the database
            # password_hash = generate_password_hash(password, method='pbkdf2:sha256')

            new_user = User(first_name=first_name, last_name=last_name, username=username, password_hash=password) #replace password with password_hash

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user :
        #and check_password_hash(user.password_hash, password): #replace password with password_hash
            # Login successful
            flash('Login successful', 'success')
            return render_template('index.html')
        else:
            # Login failed
            flash('Login failed. Please check your username and password.', 'danger')

    return render_template('login.html')

@app.route('/')
def dashboard():
    # Add logic for the dashboard route
    return render_template('index.html')

@app.route('/contactUs')
def contact():
    return render_template('contact.html')

@app.route('/aboutUs')
def aboutus():
    return render_template('about.html')

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

