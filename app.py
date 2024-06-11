import sqlite3
from datetime import datetime
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# Connect to SQLite database
conn = sqlite3.connect('vehicle_tracking.db')
cursor = conn.cursor()

# Create Vehicles table without owner_name and vehicle_model columns
cursor.execute('''
CREATE TABLE IF NOT EXISTS Vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    license_plate TEXT UNIQUE NOT NULL
)
''')

# Create Entries table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Entries (
    entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
    vehicle_id INTEGER NOT NULL,
    entry_time DATETIME NOT NULL,
    exit_time DATETIME,
    status TEXT DEFAULT 'inside',
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
)
''')

# Commit changes and close connection
conn.commit()
conn.close()

# Database connection functions
def get_db_connection():
    conn = sqlite3.connect('vehicle_tracking.db')
    conn.row_factory = sqlite3.Row  # Return rows as dictionaries
    return conn

def close_db_connection(conn):
    conn.close()

# Database operations
def add_vehicle(conn, license_plate):
    if not license_plate:
        return False  # License plate is null or empty
    
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Vehicles (license_plate) VALUES (?)", (license_plate,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Vehicle with the same license plate already exists

def add_entry(conn, vehicle_id):
    if not vehicle_id:
        return False  # Vehicle ID is null or empty
    
    entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current time
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Entries (vehicle_id, entry_time, status) VALUES (?, ?, ?)", (vehicle_id, entry_time, 'inside'))
    conn.commit()
    return True

def add_exit(conn, vehicle_id):
    if not vehicle_id:
        return False  # Vehicle ID is null or empty
    
    exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current time
    cursor = conn.cursor()
    cursor.execute("UPDATE Entries SET exit_time=?, status='outside' WHERE vehicle_id=? AND status='inside'", (exit_time, vehicle_id))
    conn.commit()
    return True

def get_vehicles_inside(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Vehicles WHERE vehicle_id IN (SELECT vehicle_id FROM Entries WHERE status='inside')")
    rows = cursor.fetchall()
    return rows

def get_vehicles_outside(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Vehicles WHERE vehicle_id IN (SELECT vehicle_id FROM Entries WHERE status='outside')")
    rows = cursor.fetchall()
    return rows

def get_vehicle_by_plate(conn, license_plate):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Vehicles WHERE license_plate=?", (license_plate,))
    row = cursor.fetchone()
    return row

def get_all_vehicles(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Vehicles")
    rows = cursor.fetchall()
    return rows

def get_vehicle_status(conn, vehicle_id):
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM Entries WHERE vehicle_id=? ORDER BY entry_time DESC LIMIT 1", (vehicle_id,))
    row = cursor.fetchone()
    if row:
        return row['status']
    else:
        return 'outside'  # Assume the vehicle is outside if no entry record is found

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/vehicles', methods=['GET'])
def vehicles_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Vehicles")
    rows = cursor.fetchall()
    vehicles = [{'vehicle_id': row['vehicle_id'], 'license_plate': row['license_plate']} for row in rows]
    close_db_connection(conn)
    return jsonify({'vehicles': vehicles})

@app.route('/vehicles', methods=['POST'])
def add_new_vehicle():
    data = request.json
    license_plate = data.get('license_plate')

    if not license_plate:
        return jsonify({'error': 'Missing input values.'}), 400
    
    conn = get_db_connection()
    success = add_vehicle(conn, license_plate)
    close_db_connection(conn)

    if success:
        return jsonify({'message': 'Vehicle added successfully.'}), 201
    else:
        return jsonify({'error': 'Vehicle with the same license plate already exists.'}), 400

@app.route('/entries', methods=['POST'])
def add_entry_exit():
    data = request.json
    license_plate = data.get('license_plate')
    entry_exit = data.get('entry_exit')  # 'entry' or 'exit'

    if not license_plate or not entry_exit:
        return jsonify({'error': 'Missing input values.'}), 400

    conn = get_db_connection()
    vehicle = get_vehicle_by_plate(conn, license_plate)
    if not vehicle:
        close_db_connection(conn)
        return jsonify({'error': 'Vehicle not found.'}), 404
    
    vehicle_id = vehicle['vehicle_id']

    # Check if the vehicle is already inside or outside
    status = get_vehicle_status(conn, vehicle_id)
    if status == 'inside' and entry_exit == 'entry':
        close_db_connection(conn)
        return jsonify({'message': 'Vehicle is already inside.'}), 200
    elif status == 'outside' and entry_exit == 'exit':
        close_db_connection(conn)
        return jsonify({'message': 'Vehicle is already outside.'}), 200

    # Proceed with adding entry or exit
    if entry_exit == 'entry':
        success = add_entry(conn, vehicle_id)
        if success:
            close_db_connection(conn)
            return jsonify({'message': 'Entry added successfully.'}), 201
        else:
            close_db_connection(conn)
            return jsonify({'error': 'Failed to add entry.'}), 500
    elif entry_exit == 'exit':
        success = add_exit(conn, vehicle_id)
        if success:
            close_db_connection(conn)
            return jsonify({'message': 'Exit added successfully.'}), 201
        else:
            close_db_connection(conn)
            return jsonify({'error': 'Failed to add exit.'}), 500
    else:
        close_db_connection(conn)
        return jsonify({'error': 'Invalid entry/exit type.'}), 400

@app.route('/vehicles/inside', methods=['GET'])
def vehicles_inside_list():
    conn = get_db_connection()
    vehicles_inside = get_vehicles_inside(conn)
    close_db_connection(conn)

    # Convert rows to dictionaries
    vehicles_inside_dicts = []
    for vehicle in vehicles_inside:
        vehicle_dict = dict(vehicle)
        vehicles_inside_dicts.append(vehicle_dict)

    return jsonify({'vehicles_inside': vehicles_inside_dicts})

@app.route('/vehicles/outside', methods=['GET'])
def vehicles_outside_list():
    conn = get_db_connection()
    vehicles_outside = get_vehicles_outside(conn)
    close_db_connection(conn)

    # Convert rows to dictionaries
    vehicles_outside_dicts = []
    for vehicle in vehicles_outside:
        vehicle_dict = dict(vehicle)
        vehicles_outside_dicts.append(vehicle_dict)

    return jsonify({'vehicles_outside': vehicles_outside_dicts})

@app.route('/vehicles/activity/<string:license_plate>', methods=['GET'])
def vehicle_activity(license_plate):
    conn = get_db_connection()
    vehicle = get_vehicle_by_plate(conn, license_plate)
    if not vehicle:
        close_db_connection(conn)
        return jsonify({'error': 'Vehicle not found.'}), 404
    
    vehicle_id = vehicle['vehicle_id']
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Entries WHERE vehicle_id=? ORDER BY entry_time DESC", (vehicle_id,))
    activity_rows = cursor.fetchall()
    close_db_connection(conn)

    # Convert rows to dictionaries
    activity_dicts = []
    for row in activity_rows:
        activity_dict = dict(row)
        activity_dicts.append(activity_dict)

    return jsonify({'vehicle_activity': activity_dicts})

@app.route('/recent_activities', methods=['GET'])
def recent_activities():
    page = int(request.args.get('page', 1))
    per_page = 10
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get total count of activity records
    cursor.execute("SELECT COUNT(*) FROM Entries")
    total_count = cursor.fetchone()[0]
    total_pages = (total_count + per_page - 1) // per_page
    
    # Fetch recent activity records with pagination
    offset = (page - 1) * per_page
    cursor.execute("""
        SELECT Vehicles.license_plate, Entries.entry_time, Entries.exit_time
        FROM Entries
        JOIN Vehicles ON Entries.vehicle_id = Vehicles.vehicle_id
        ORDER BY Entries.entry_time DESC
        LIMIT ? OFFSET ?
    """, (per_page, offset))
    activity_rows = cursor.fetchall()
    close_db_connection(conn)
    
    # Convert rows to dictionaries
    activities = [dict(row) for row in activity_rows]

    return jsonify({
        'activities': activities,
        'total_pages': total_pages,
        'current_page': page
    })

# Main
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
