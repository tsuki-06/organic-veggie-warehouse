from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DATABASE = os.path.join(os.path.dirname(__file__), 'warehouse.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT sb.batch_id, v.veg_name, f.name, sz.zone_name, sb.quantity, sb.receive_date, sb.expiry_date
        FROM Stock_Batches sb
        JOIN Vegetables v ON sb.veg_id = v.veg_id
        JOIN Farmers f ON sb.farmer_id = f.farmer_id
        JOIN Storage_Zones sz ON sb.zone_id = sz.zone_id
    """)
    batches = cur.fetchall()
    conn.close()
    return render_template('index.html', batches=batches)

@app.route('/vegetables')
def vegetables():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM Vegetables")
    veggies = cur.fetchall()
    conn.close()
    return render_template('vegetables.html', veggies=veggies)

@app.route('/vegetables/add', methods=['GET', 'POST'])
def add_vegetable():
    if request.method == 'POST':
        veg_name = request.form['veg_name']
        category = request.form['category']
        storage_temp = request.form['storage_temp']
        farmer_id = request.form.get('farmer_id')
        new_farmer_name = request.form.get('new_farmer_name', '').strip()
        new_farmer_phone = request.form.get('new_farmer_phone', '').strip()
        new_farmer_address = request.form.get('new_farmer_address', '').strip()
        zone_id = request.form['zone_id']
        quantity = request.form['quantity']
        receive_date = request.form['receive_date']
        expiry_date = request.form['expiry_date']
        
        conn = get_db()
        cur = conn.cursor()
        
        # Handle farmer - either existing or new
        if new_farmer_name:
            # Check if farmer already exists
            cur.execute("SELECT farmer_id FROM Farmers WHERE name = ?", (new_farmer_name,))
            existing_farmer = cur.fetchone()
            if existing_farmer:
                farmer_id = existing_farmer[0]
            else:
                # Insert new farmer
                cur.execute("INSERT INTO Farmers (name, phone, address) VALUES (?, ?, ?)", (new_farmer_name, new_farmer_phone, new_farmer_address))
                farmer_id = cur.lastrowid
        
        # Insert vegetable
        cur.execute("INSERT INTO Vegetables (veg_name, category, storage_temp) VALUES (?, ?, ?)", (veg_name, category, storage_temp))
        veg_id = cur.lastrowid
        
        # Insert stock batch
        cur.execute("INSERT INTO Stock_Batches (veg_id, farmer_id, zone_id, quantity, receive_date, expiry_date) VALUES (?, ?, ?, ?, ?, ?)", 
                   (veg_id, farmer_id, zone_id, quantity, receive_date, expiry_date))
        
        # Insert transaction
        batch_id = cur.lastrowid
        cur.execute("INSERT INTO Transactions (batch_id, transaction_type, qty_changed, transaction_date) VALUES (?, 'IN', ?, ?)", 
                   (batch_id, quantity, receive_date))
        
        conn.commit()
        conn.close()
        return redirect(url_for('vegetables'))
    
    # Get farmers and zones for dropdowns
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT farmer_id, name FROM Farmers")
    farmers = cur.fetchall()
    cur.execute("SELECT zone_id, zone_name FROM Storage_Zones")
    zones = cur.fetchall()
    conn.close()
    
    return render_template('add_vegetable.html', farmers=farmers, zones=zones)

@app.route('/vegetables/edit/<int:id>', methods=['GET', 'POST'])
def edit_vegetable(id):
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        veg_name = request.form['veg_name']
        category = request.form['category']
        storage_temp = request.form['storage_temp']
        cur.execute("UPDATE Vegetables SET veg_name=?, category=?, storage_temp=? WHERE veg_id=?", (veg_name, category, storage_temp, id))
        conn.commit()
        conn.close()
        return redirect(url_for('vegetables'))
    cur.execute("SELECT * FROM Vegetables WHERE veg_id=?", (id,))
    veggie = cur.fetchone()
    conn.close()
    return render_template('edit_vegetable.html', veggie=veggie)

@app.route('/vegetables/delete/<int:id>', methods=['POST'])
def delete_vegetable(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM Vegetables WHERE veg_id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('vegetables'))

if __name__ == '__main__':
    app.run(debug=True)