CREATE TABLE Customer (
    customer_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone_number VARCHAR(20),
    address VARCHAR(255)
);

CREATE TABLE Car (
    car_id SERIAL PRIMARY KEY,
    make VARCHAR(50),
    model VARCHAR(50),
    year INTEGER,
    color VARCHAR(20),
    license_plate VARCHAR(20),
    rental_rate_per_day DECIMAL(10, 2),
    available BOOLEAN
);

CREATE TABLE Rental (
    rental_id SERIAL PRIMARY KEY,
    customer_id INTEGER REFERENCES Customer(customer_id),
    car_id INTEGER REFERENCES Car(car_id),
    start_date DATE,
    end_date DATE,
    total_cost DECIMAL(10, 2)
);
