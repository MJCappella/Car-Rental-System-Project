from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysupersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:mjay0001@localhost/carrental'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

conn = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "mjay0001"
)

cur = conn.cursor()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.varchar(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('Password and Confirm Password do not match. Please try again.', 'danger')
        else:
            # Hash the password before storing it in the database
            # password_hash = generate_password_hash(password, method='pbkdf2:sha256')

            new_user = User(first_name=first_name, last_name=last_name, email=email, password_hash=password) #replace password with password_hash

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user :
        #and check_password_hash(user.password_hash, password): #replace password with password_hash
            # Login successful
            flash('Login successful', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Login failed
            flash('Login failed. Please check your email and password.', 'danger')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Add logic for the dashboard route
    return render_template('index.html')

@app.route('/admin')
def admin_dashboard():
    # Connect to the database and fetch system statistics
    cur.execute("SELECT COUNT(*) FROM customer")
    total_customers = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM car")
    total_cars = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM rental")
    total_rentals = cur.fetchone()[0]
    conn.close()
    return render_template('admin_dashboard.html', total_customers=total_customers, total_cars=total_cars, total_rentals=total_rentals)

@app.route('/admin/customers')
def manage_customers():
    # Connect to the database and fetch all customers
    cur.execute("SELECT * FROM customer")
    customers = cur.fetchall()
    conn.close()
    return render_template('manage_customers.html', customers=customers)

@app.route('/admin/cars')
def manage_cars():
    # Connect to the database and fetch all cars
    cur.execute("SELECT * FROM car")
    cars = cur.fetchall()
    conn.close()
    return render_template('manage_cars.html', cars=cars)

@app.route('/admin/rentals')
def manage_rentals():
    # Connect to the database and fetch all rentals
    cur.execute("SELECT * FROM rental")
    rentals = cur.fetchall()
    conn.close()
    return render_template('manage_rentals.html', rentals=rentals)

@app.route('/admin/add_car', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        color = request.form['color']
        license_plate = request.form['license_plate']
        rental_rate_per_day = request.form['rental_rate_per_day']
        available = request.form.get('available', False)
        cur.execute("INSERT INTO car (make, model, year, color, license_plate, rental_rate_per_day, available) VALUES (%s, %s, %s, %s, %s, %s, %s)", (make, model, year, color, license_plate, rental_rate_per_day, available))
        conn.commit()
        conn.close()
        flash('Car added successfully', 'success')
        return redirect(url_for('manage_cars'))
    return render_template('add_car.html')

@app.route('/admin/edit_car/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    if request.method == 'POST':
        make = request.form['make']
        model = request.form['model']
        year = request.form['year']
        color = request.form['color']
        license_plate = request.form['license_plate']
        rental_rate_per_day = request.form['rental_rate_per_day']
        available = request.form.get('available', False)
        cur.execute("UPDATE car SET make=%s, model=%s, year=%s, color=%s, license_plate=%s, rental_rate_per_day=%s, available=%s WHERE car_id=%s", (make, model, year, color, license_plate, rental_rate_per_day, available, car_id))
        conn.commit()
        conn.close()
        flash('Car updated successfully', 'success')
        return redirect(url_for('manage_cars'))
    cur.execute("SELECT * FROM car WHERE car_id = %s", (car_id,))
    car = cur.fetchone()
    conn.close()
    return render_template('edit_car.html', car=car)

@app.route('/admin/delete_car/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    cur.execute("DELETE FROM car WHERE car_id = %s", (car_id,))
    conn.commit()
    conn.close()
    flash('Car deleted successfully', 'success')
    return redirect(url_for('manage_cars'))

@app.route('/admin/add_rental', methods=['GET', 'POST'])
def add_rental():
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        car_id = request.form['car_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        total_cost = request.form['total_cost']
        cur.execute("INSERT INTO rental (customer_id, car_id, start_date, end_date, total_cost) VALUES (%s, %s, %s, %s, %s)", (customer_id, car_id, start_date, end_date, total_cost))
        conn.commit()
        conn.close()
        flash('Rental added successfully', 'success')
        return redirect(url_for('manage_rentals'))
    return render_template('add_rental.html')

@app.route('/admin/edit_rental/<int:rental_id>', methods=['GET', 'POST'])
def edit_rental(rental_id):
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        car_id = request.form['car_id']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        total_cost = request.form['total_cost']
        cur.execute("UPDATE rental SET customer_id=%s, car_id=%s, start_date=%s, end_date=%s, total_cost=%s WHERE rental_id=%s", (customer_id, car_id, start_date, end_date, total_cost, rental_id))
        conn.commit()
        conn.close()
        flash('Rental updated successfully', 'success')
        return redirect(url_for('manage_rentals'))
    cur.execute("SELECT * FROM rental WHERE rental_id = %s", (rental_id,))
    rental = cur.fetchone()
    conn.close()
    return render_template('edit_rental.html', rental=rental)

@app.route('/admin/delete_rental/<int:rental_id>', methods=['POST'])
def delete_rental(rental_id):
    cur.execute("DELETE FROM rental WHERE rental_id = %s", (rental_id,))
    conn.commit()
    conn.close()
    flash('Rental deleted successfully', 'success')
    return redirect(url_for('manage_rentals'))

if __name__ == '__main__':
    # When running this script directly, create the database tables
    with app.app_context():
        db.create_all()
    app.run(debug=True)