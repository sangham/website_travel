from flask import Flask, request, jsonify, render_template
import sqlite3
import os
from datetime import datetime
from flask_cors import CORS 

app = Flask(__name__)
CORS(app) 

# Database setup - Modified for Vercel
def get_db_connection():
    # On Vercel, we need to handle database differently
    conn = sqlite3.connect('/tmp/visitors.db')
    return conn

def init_db():
    conn = get_db_connection()
    c = conn.cursor()
    
    # Visitors table
    c.execute('''CREATE TABLE IF NOT EXISTS visitors
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT,
                  phone TEXT NOT NULL,
                  interest TEXT,
                  message TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Bookings table
    c.execute('''CREATE TABLE IF NOT EXISTS bookings
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  email TEXT,
                  phone TEXT NOT NULL,
                  pickup_location TEXT,
                  drop_location TEXT,
                  passengers INTEGER,
                  message TEXT,
                  timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Vehicles table
    c.execute('''CREATE TABLE IF NOT EXISTS vehicles
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  image_url TEXT,
                  description TEXT,
                  capacity INTEGER,
                  price_per_km REAL,
                  features TEXT,
                  fuel_type TEXT,
                  transmission TEXT,
                  luggage_capacity TEXT)''')
    
    # Packages table
    c.execute('''CREATE TABLE IF NOT EXISTS packages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  image_url TEXT,
                  description TEXT,
                  duration TEXT,
                  price REAL,
                  itinerary TEXT,
                  inclusions TEXT,
                  exclusions TEXT,
                  highlights TEXT)''')
    
    # Blogs table
    c.execute('''CREATE TABLE IF NOT EXISTS blogs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  title TEXT NOT NULL,
                  image_url TEXT,
                  content TEXT,
                  excerpt TEXT,
                  author TEXT,
                  publish_date DATE,
                  category TEXT)''')
    
    # Char Dham Packages table
    c.execute('''CREATE TABLE IF NOT EXISTS char_dham_packages
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  duration TEXT,
                  price REAL,
                  description TEXT,
                  itinerary TEXT,
                  inclusions TEXT,
                  exclusions TEXT,
                  highlights TEXT)''')
    
    # Insert sample vehicles
    c.execute("SELECT COUNT(*) FROM vehicles")
    if c.fetchone()[0] == 0:
        vehicles = [
            ('Toyota Innova Crysta', '/static/images/vehicles/innova-crysta.jpg', 
             'Luxury MPV with comfortable seating for 7 passengers, perfect for family trips and long journeys.', 
             7, 15.0, 'AC, Power Steering, Music System, Airbags, GPS, Rear Camera, Sunroof', 'Diesel', 'Manual', '4 Large Bags + 2 Small Bags'),
            ('Kia Carens', '/static/images/vehicles/kia-carens.jpg', 
             'Spacious family car with modern features and excellent comfort for city and highway travel.', 
             7, 14.0, 'AC, Power Windows, Touchscreen, Rear Camera, Sunroof, Bluetooth, Climate Control', 'Petrol', 'Automatic', '3 Large + 2 Small Bags'),
            ('Toyota Rumion', '/static/images/vehicles/toyota-rumion.jpg', 
             'Compact MPV with great fuel efficiency and comfortable interior for budget-conscious travelers.', 
             7, 13.5, 'AC, Power Steering, Bluetooth, Central Locking, Music System, Power Windows', 'Petrol', 'Manual', '3 Large Bags'),
            ('Maruti Ertiga', '/static/images/vehicles/maruti-ertiga.jpg', 
             'Popular MPV known for reliability, low maintenance, and excellent fuel economy.', 
             7, 12.0, 'AC, Power Steering, Music System, Air Conditioning, Central Locking, Power Windows', 'Petrol', 'Manual', '3 Large Bags'),
        ]
        c.executemany("INSERT INTO vehicles (name, image_url, description, capacity, price_per_km, features, fuel_type, transmission, luggage_capacity) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", vehicles)
    
    # Insert Char Dham packages
    c.execute("SELECT COUNT(*) FROM char_dham_packages")
    if c.fetchone()[0] == 0:
        packages = [
            ('Basic Package', '12 Days / 11 Nights', 25999,
             'Standard accommodation with all essential services for a comfortable spiritual journey.',
             'Day 1: Haridwar|Day 2: Haridwar to Barkot|Day 3: Yamunotri|Day 4: Barkot to Uttarkashi|Day 5: Gangotri|Day 6: Uttarkashi to Guptkashi|Day 7: Kedarnath|Day 8: Kedarnath to Guptkashi|Day 9: Badrinath|Day 10: Badrinath to Rudraprayag|Day 11: Rishikesh|Day 12: Departure',
             'Accommodation, All Meals, Transportation, Guide Services, Basic Medical Kit',
             'Helicopter Services, Porter Services, Personal Expenses, Travel Insurance',
             'All Four Dhams, Ganga Aarti, Spiritual Guide, Comfortable Travel'),
            
            ('Standard Package', '12 Days / 11 Nights', 35999,
             'Enhanced comfort with better accommodation and additional services for a smoother pilgrimage.',
             'Day 1: Haridwar|Day 2: Haridwar to Barkot|Day 3: Yamunotri|Day 4: Barkot to Uttarkashi|Day 5: Gangotri|Day 6: Uttarkashi to Guptkashi|Day 7: Kedarnath|Day 8: Kedarnath to Guptkashi|Day 9: Badrinath|Day 10: Badrinath to Rudraprayag|Day 11: Rishikesh|Day 12: Departure',
             '3-Star Accommodation, All Meals, AC Transportation, Experienced Guide, Medical Assistance, Porter Services',
             'Helicopter Services, Luxury Accommodation, Personal Shopping, Travel Insurance',
             'All Four Dhams, VIP Darshan, Expert Spiritual Guide, Porter Support'),
            
            ('Premium Package', '10 Days / 9 Nights', 49999,
             'Luxury pilgrimage experience with helicopter services and premium accommodations.',
             'Day 1: Haridwar|Day 2: Haridwar to Barkot|Day 3: Yamunotri|Day 4: Gangotri|Day 5: Guptkashi|Day 6: Kedarnath by Helicopter|Day 7: Badrinath|Day 8: Badrinath to Rudraprayag|Day 9: Rishikesh|Day 10: Departure',
             'Luxury Accommodation, All Meals, Luxury AC Vehicle, Helicopter for Kedarnath, Expert Guide, Medical Support, Porter & Pony Services',
             'Personal Expenses, Travel Insurance, Luxury Shopping',
             'Helicopter Experience, Luxury Stays, VIP Darshan, Personalized Service')
        ]
        c.executemany("INSERT INTO char_dham_packages (name, duration, price, description, itinerary, inclusions, exclusions, highlights) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", packages)
    
    # Insert sample packages
    c.execute("SELECT COUNT(*) FROM packages")
    if c.fetchone()[0] == 0:
        packages = [
            ('Dehradun to Chandigarh', '/static/images/packages/chandigarh.jpg', 
             'Comfortable ride to the beautiful city of Chandigarh, known for its architecture and gardens.', 
             '2 Days, 1 Night', 3500, 
             'Day 1: Pickup from Dehradun, travel to Chandigarh, visit Rock Garden and Sukhna Lake|Day 2: Explore Rose Garden and Sector 17 market, return to Dehradun',
             'AC Vehicle, Driver Allowance, Fuel Charges, Toll Taxes, Parking Charges, GST',
             'Meals, Accommodation, Entry Fees, Personal Expenses, Guide Charges',
             'Rock Garden Visit, Sukhna Lake, Rose Garden, Shopping at Sector 17, City Architecture'),
            
            ('Dehradun to Mussoorie', '/static/images/packages/mussoorie.jpg', 
             'Beautiful hill station known as Queen of Hills with stunning views and pleasant climate.', 
             '2 Days, 1 Night', 2500,
             'Day 1: Dehradun to Mussoorie, visit Kempty Falls, Gun Hill|Day 2: Lal Tibba, Company Garden, Mall Road, return to Dehradun',
             'AC Vehicle, Driver, Fuel, Toll, Parking, GST',
             'Hotel, Meals, Entry Fees, Personal Expenses, Guide Charges',
             'Kempty Falls, Gun Hill, Mall Road, Scenic Views, Cable Car Ride')
        ]
        c.executemany("INSERT INTO packages (name, image_url, description, duration, price, itinerary, inclusions, exclusions, highlights) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", packages)
    
    # Insert sample blogs
    c.execute("SELECT COUNT(*) FROM blogs")
    if c.fetchone()[0] == 0:
        blogs = [
            ('Complete Guide to Char Dham Yatra 2024', 
             '/static/images/blogs/char-dham-guide.jpg',
             '''
             <h2>Introduction to Char Dham Yatra</h2>
             <p>The Char Dham Yatra is one of the most sacred pilgrimage circuits in Hinduism, covering four holy sites in the Garhwal region of Uttarakhand.</p>
             
             <h2>Best Time to Visit</h2>
             <p>The ideal time for Char Dham Yatra is from April/May to October/November.</p>
             ''',
             'Complete guide to planning your Char Dham Yatra in 2024 with route details, best time to visit, and essential tips.',
             'Rajesh Kumar', '2024-01-15', 'Pilgrimage')
        ]
        c.executemany("INSERT INTO blogs (title, image_url, content, excerpt, author, publish_date, category) VALUES (?, ?, ?, ?, ?, ?, ?)", blogs)
    
    conn.commit()
    conn.close()

# Initialize database on first request
@app.before_first_request
def initialize():
    init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vehicles')
def vehicles():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM vehicles")
    vehicles = c.fetchall()
    conn.close()
    return render_template('vehicles.html', vehicles=vehicles)

@app.route('/vehicle/<int:vehicle_id>')
def vehicle_detail(vehicle_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
    vehicle = c.fetchone()
    conn.close()
    
    if vehicle:
        vehicle_dict = {
            'id': vehicle[0],
            'name': vehicle[1],
            'image_url': vehicle[2],
            'description': vehicle[3],
            'capacity': vehicle[4],
            'price_per_km': vehicle[5],
            'features': vehicle[6].split(', ') if vehicle[6] else [],
            'fuel_type': vehicle[7],
            'transmission': vehicle[8],
            'luggage_capacity': vehicle[9]
        }
        return render_template('vehicle-detail.html', vehicle=vehicle_dict)
    else:
        return "Vehicle not found", 404

@app.route('/vacation-packages')
def vacation_packages():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM packages")
    packages = c.fetchall()
    conn.close()
    return render_template('vacation-packages.html', packages=packages)

@app.route('/package/<int:package_id>')
def package_detail(package_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM packages WHERE id = ?", (package_id,))
    package = c.fetchone()
    conn.close()
    
    if package:
        package_dict = {
            'id': package[0],
            'name': package[1],
            'image_url': package[2],
            'description': package[3],
            'duration': package[4],
            'price': package[5],
            'itinerary': package[6].split('|') if package[6] else [],
            'inclusions': package[7].split(', ') if package[7] else [],
            'exclusions': package[8].split(', ') if package[8] else [],
            'highlights': package[9].split(', ') if package[9] else []
        }
        return render_template('package-detail.html', package=package_dict)
    else:
        return "Package not found", 404

@app.route('/char-dham-yatra')
def char_dham_yatra():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM char_dham_packages")
    packages = c.fetchall()
    conn.close()
    
    packages_list = []
    for package in packages:
        packages_list.append({
            'id': package[0],
            'name': package[1],
            'duration': package[2],
            'price': package[3],
            'description': package[4],
            'itinerary': package[5].split('|') if package[5] else [],
            'inclusions': package[6].split(', ') if package[6] else [],
            'exclusions': package[7].split(', ') if package[7] else [],
            'highlights': package[8].split(', ') if package[8] else []
        })
    
    return render_template('char-dham-yatra.html', packages=packages_list)

@app.route('/char-dham-booking', methods=['POST'])
def char_dham_booking():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        
        # Save booking to database
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO bookings (name, email, phone, pickup_location, drop_location, passengers, message) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (data['name'], data.get('email', ''), data['phone'], 
                   data.get('pickup_location', ''), data.get('drop_location', ''), 
                   data.get('passengers', 1), data.get('message', '')))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Your Char Dham Yatra booking has been submitted successfully!"})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/blogs')
def blogs():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM blogs ORDER BY publish_date DESC")
    blogs = c.fetchall()
    conn.close()
    
    blog_list = []
    for blog in blogs:
        blog_list.append({
            'id': blog[0],
            'title': blog[1],
            'image_url': blog[2],
            'content': blog[3],
            'excerpt': blog[4],
            'author': blog[5],
            'publish_date': blog[6],
            'category': blog[7]
        })
    
    return render_template('blogs.html', blogs=blog_list)

@app.route('/blog/<int:blog_id>')
def blog_detail(blog_id):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM blogs WHERE id = ?", (blog_id,))
    blog = c.fetchone()
    conn.close()
    
    if blog:
        blog_dict = {
            'id': blog[0],
            'title': blog[1],
            'image_url': blog[2],
            'content': blog[3],
            'excerpt': blog[4],
            'author': blog[5],
            'publish_date': blog[6],
            'category': blog[7]
        }
        return render_template('blog-detail.html', blog=blog_dict)
    else:
        return "Blog not found", 404

@app.route('/api/submit-visitor', methods=['POST'])
def submit_visitor():
    try:
        data = request.json
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO visitors (name, email, phone, interest, message) VALUES (?, ?, ?, ?, ?)",
                  (data['name'], data.get('email', ''), data['phone'], data['interest'], data.get('message', '')))
        conn.commit()
        conn.close()
        return jsonify({"status": "success", "message": "Visitor information stored successfully"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/contact-us')
def contact_us():
    return render_template('contact-us.html')

@app.route('/api/submit-contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        
        # Save to database
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO visitors (name, email, phone, interest, message) VALUES (?, ?, ?, ?, ?)",
                  (data['name'], data['email'], data['phone'], data['subject'], data['message']))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Your message has been sent successfully!"})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/char-dham/<dham_name>')
def char_dham_detail(dham_name):
    dham_data = {
        'yamunotri': {
            'name': 'Yamunotri',
            'title': 'Yamunotri Dham - Source of Yamuna River',
            'image': 'https://royaltourr.com/wp-content/uploads/2025/06/Yamunotri-Dham-1024x512.jpg',
            'altitude': '3,293 meters',
            'best_time': 'May to October',
            'main_temple': 'Yamunotri Temple',
            'significance': 'Source of Yamuna River',
            'description': 'Yamunotri is the source of the Yamuna River and the seat of the goddess Yamuna. It is the first stop in the Char Dham Yatra circuit located in the Garhwal Himalayas.',
            'detailed_info': '''
            <h3>About Yamunotri</h3>
            <p>Yamunotri is the source of the Yamuna River and the seat of the goddess Yamuna in Hinduism. It is one of the four sites in India's Char Dham pilgrimage.</p>
            '''
        },
        'gangotri': {
            'name': 'Gangotri',
            'title': 'Gangotri Dham - Origin of Ganges River',
            'image': 'https://royaltourr.com/wp-content/uploads/2025/06/Gangotri-Yatra.jpg',
            'altitude': '3,100 meters',
            'best_time': 'May to October',
            'main_temple': 'Gangotri Temple',
            'significance': 'Origin of Ganga River',
            'description': 'Gangotri is the origin of the holy Ganges River, where Goddess Ganga descended to earth. It is the second destination in the Char Dham pilgrimage.',
            'detailed_info': '''
            <h3>About Gangotri</h3>
            <p>Gangotri is a town and a Nagar Panchayat in Uttarkashi district of Uttarakhand. It is a Hindu pilgrim town on the banks of the river Bhagirathi.</p>
            '''
        },
        'kedarnath': {
            'name': 'Kedarnath',
            'title': 'Kedarnath Temple - Jyotirlinga of Shiva',
            'image': 'https://royaltourr.com/wp-content/uploads/2025/06/kedarnath-temple-1536x768.jpg',
            'altitude': '3,583 meters',
            'best_time': 'May to October',
            'main_temple': 'Kedarnath Temple',
            'significance': 'Jyotirlinga of Shiva',
            'description': 'Kedarnath is one of the twelve Jyotirlingas of Lord Shiva, situated near the Mandakini River in the Himalayas.',
            'detailed_info': '''
            <h3>About Kedarnath</h3>
            <p>Kedarnath is a Hindu temple dedicated to Lord Shiva. Located on the Garhwal Himalayan range near the Mandakini river, it is one of the twelve Jyotirlingas.</p>
            '''
        },
        'badrinath': {
            'name': 'Badrinath',
            'title': 'Badrinath Temple - Abode of Lord Vishnu',
            'image': 'https://royaltourr.com/wp-content/uploads/2025/06/badrinath-temple-1536x768.jpeg',
            'altitude': '3,133 meters',
            'best_time': 'May to October',
            'main_temple': 'Badrinath Temple',
            'significance': 'Abode of Lord Vishnu',
            'description': 'Badrinath is dedicated to Lord Vishnu and is situated along the banks of the Alaknanda River. It is the final destination of the Char Dham Yatra.',
            'detailed_info': '''
            <h3>About Badrinath</h3>
            <p>Badrinath is a town and nagar panchayat in Chamoli district of Uttarakhand. It is the most important of the four sites in India's Char Dham pilgrimage.</p>
            '''
        }
    }
    
    dham = dham_data.get(dham_name)
    if not dham:
        return "Dham not found", 404
    
    return render_template('char-dham-detail.html', dham=dham)

@app.route('/api/submit-booking', methods=['POST'])
def submit_booking():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"status": "error", "message": "No data provided"}), 400
        
        # Save booking to database
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("INSERT INTO bookings (name, email, phone, pickup_location, drop_location, passengers, message) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (data['name'], data.get('email', ''), data['phone'], 
                   data.get('pickup', ''), data.get('drop', ''), 
                   data.get('passengers', 1), data.get('message', '')))
        conn.commit()
        conn.close()
        
        return jsonify({"status": "success", "message": "Your booking request has been submitted successfully! We will contact you shortly."})
        
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/book-now')
def book_now():
    return render_template('contact-us.html')

# Vercel requires this
app = app