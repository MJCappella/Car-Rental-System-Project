from flask import Flask, render_template, request, redirect, url_for
import psycopg2  # assuming PostgreSQL is used as the database

app = Flask(__name__)

# Database connection parameters
DB_HOST = 'your_database_host'
DB_NAME = 'your_database_name'
DB_USER = 'your_database_user'
DB_PASSWORD = 'your_database_password'

# Define routes

@app.route('/admin')
def admin_dashboard():
    # Connect to the database and fetch system statistics
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
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
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute("SELECT * FROM customer")
    customers = cur.fetchall()
    conn.close()
    return render_template('manage_customers.html', customers=customers)

@app.route('/admin/cars')
def manage_cars():
    # Connect to the database and fetch all cars
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute("SELECT * FROM car")
    cars = cur.fetchall()
    conn.close()
    return render_template('manage_cars.html', cars=cars)

@app.route('/admin/rentals')
def manage_rentals():
    # Connect to the database and fetch all rentals
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
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
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute("INSERT INTO car (make, model, year, color, license_plate, rental_rate_per_day, available) VALUES (%s, %s, %s, %s, %s, %s, %s)", (make, model, year, color, license_plate, rental_rate_per_day, available))
        conn.commit()
        conn.close()
        flash('Car added successfully', 'success')
        return redirect(url_for('manage_cars'))
    return render_template('add_car.html')

@app.route('/admin/edit_car/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
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
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
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
        conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute("INSERT INTO rental (customer_id, car_id, start_date, end_date, total_cost) VALUES (%s, %s, %s, %s, %s)", (customer_id, car_id, start_date, end_date, total_cost))
        conn.commit()
        conn.close()
        flash('Rental added successfully', 'success')
        return redirect(url_for('manage_rentals'))
    return render_template('add_rental.html')

@app.route('/admin/edit_rental/<int:rental_id>', methods=['GET', 'POST'])
def edit_rental(rental_id):
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
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
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute("DELETE FROM rental WHERE rental_id = %s", (rental_id,))
    conn.commit()
    conn.close()
    flash('Rental deleted successfully', 'success')
    return redirect(url_for('manage_rentals'))


# Add routes for adding, editing, and deleting customers, cars, and rentals

if __name__ == '__main__':
    app.run(debug=True)
