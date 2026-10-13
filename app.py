from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path
from datetime import date

app = Flask(__name__)
app.secret_key = "change-this-secret-key"
DB_PATH = Path(__file__).with_name("rental.db")

CARS = [
    {"id": "swift", "name": "Maruti Suzuki Swift", "category": "Hatchback", "price": 1800, "seats": 5, "fuel": "Petrol", "transmission": "Manual", "image": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?auto=format&fit=crop&w=1000&q=80", "description": "Compact, easy to drive and ideal for city trips."},
    {"id": "city", "name": "Honda City", "category": "Sedan", "price": 2800, "seats": 5, "fuel": "Petrol", "transmission": "Automatic", "image": "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=1000&q=80", "description": "Comfortable space for business and family travel."},
    {"id": "creta", "name": "Hyundai Creta", "category": "SUV", "price": 3500, "seats": 5, "fuel": "Diesel", "transmission": "Automatic", "image": "https://images.unsplash.com/photo-1519641471654-76ce0107ad1b?auto=format&fit=crop&w=1000&q=80", "description": "A spacious SUV for longer journeys and weekend escapes."},
    {"id": "innova", "name": "Toyota Innova Crysta", "category": "MUV", "price": 4200, "seats": 7, "fuel": "Diesel", "transmission": "Manual", "image": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?auto=format&fit=crop&w=1000&q=80", "description": "Extra room for group trips, luggage and family holidays."},
]
CAR_BY_ID = {car["id"]: car for car in CARS}

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                car_id TEXT NOT NULL,
                pickup_location TEXT NOT NULL,
                drop_location TEXT NOT NULL,
                pickup_date TEXT NOT NULL,
                pickup_time TEXT NOT NULL,
                return_date TEXT NOT NULL,
                return_time TEXT NOT NULL,
                driver_age INTEGER NOT NULL,
                license_number TEXT NOT NULL,
                payment_method TEXT NOT NULL,
                extras TEXT,
                notes TEXT,
                estimated_total INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

@app.context_processor
def inject_globals():
    return {"today": date.today().isoformat()}

@app.route("/")
def home():
    return render_template("index.html", cars=CARS[:3])

@app.route("/cars")
def cars():
    return render_template("cars.html", cars=CARS)

@app.route("/booking", methods=["GET", "POST"])
def booking():
    selected_car = request.args.get("car", "")
    if request.method == "POST":
        fields = ["full_name", "email", "phone", "car_id", "pickup_location", "drop_location",
                  "pickup_date", "pickup_time", "return_date", "return_time", "driver_age",
                  "license_number", "payment_method"]
        data = {field: request.form.get(field, "").strip() for field in fields}
        extras = request.form.getlist("extras")
        notes = request.form.get("notes", "").strip()

        missing = [field for field in fields if not data[field]]
        if missing:
            flash("Please complete all required fields.", "error")
            return render_template("booking.html", cars=CARS, selected_car=data.get("car_id", selected_car))

        car = CAR_BY_ID.get(data["car_id"])
        if not car:
            flash("Please choose a valid car.", "error")
            return render_template("booking.html", cars=CARS, selected_car=selected_car)

        try:
            age = int(data["driver_age"])
            if age < 18 or age > 100:
                raise ValueError
            start = date.fromisoformat(data["pickup_date"])
            end = date.fromisoformat(data["return_date"])
            days = (end - start).days
            if days < 1:
                flash("Return date must be at least one day after pickup date.", "error")
                return render_template("booking.html", cars=CARS, selected_car=data["car_id"])
            if start < date.today():
                flash("Pickup date cannot be in the past.", "error")
                return render_template("booking.html", cars=CARS, selected_car=data["car_id"])
        except ValueError:
            flash("Check the driver age and rental dates. Driver must be 18 or older.", "error")
            return render_template("booking.html", cars=CARS, selected_car=data["car_id"])

        total = days * car["price"] + (500 if "child-seat" in extras else 0) + (300 if "wifi" in extras else 0)
        with get_db() as conn:
            cur = conn.execute("""
                INSERT INTO bookings
                (full_name,email,phone,car_id,pickup_location,drop_location,pickup_date,pickup_time,
                 return_date,return_time,driver_age,license_number,payment_method,extras,notes,estimated_total)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            """, (data["full_name"], data["email"], data["phone"], data["car_id"],
                  data["pickup_location"], data["drop_location"], data["pickup_date"], data["pickup_time"],
                  data["return_date"], data["return_time"], age, data["license_number"],
                  data["payment_method"], ", ".join(extras), notes, total))
            booking_id = cur.lastrowid
        return render_template("confirmation.html", booking_id=booking_id, data=data, car=car,
                               days=days, total=total, extras=extras)

    return render_template("booking.html", cars=CARS, selected_car=selected_car)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()
        if not all([name, email, subject, message]):
            flash("Please fill in every field.", "error")
        else:
            with get_db() as conn:
                conn.execute("INSERT INTO messages (name,email,subject,message) VALUES (?,?,?,?)",
                             (name, email, subject, message))
            flash("Message saved successfully. Our demo team will be in touch.", "success")
            return redirect(url_for("contact"))
    return render_template("contact.html")

@app.route("/admin")
def admin():
    # Simple classroom/demo dashboard; add authentication before any real deployment.
    with get_db() as conn:
        bookings = conn.execute("SELECT * FROM bookings ORDER BY id DESC").fetchall()
        messages = conn.execute("SELECT * FROM messages ORDER BY id DESC").fetchall()
    return render_template("admin.html", bookings=bookings, messages=messages, cars=CAR_BY_ID)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html"), 404

init_db()

if __name__ == "__main__":
    app.run(debug=True)
