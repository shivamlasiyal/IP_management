from flask import Flask, request, render_template, redirect, url_for, send_file
import sqlite3
import pandas as pd
import io
from io import BytesIO

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=('GET', 'POST'))
def index():
    conn = get_db_connection()
    ip_records = conn.execute('SELECT * FROM ip_records').fetchall()

    if request.method == 'POST':
        machine_name = request.form['machine_name']
        ip_address = request.form['ip_address']

        if 'add' in request.form:
            conn.execute('INSERT INTO ip_records (machine_name, ip_address) VALUES (?, ?)', (machine_name, ip_address))
            conn.commit()
        elif 'delete' in request.form:
            id = request.form['delete']
            conn.execute('DELETE FROM ip_records WHERE id = ?', (id,))
            conn.commit()
        elif 'update' in request.form:
            id = request.form['id']
            conn.execute('UPDATE ip_records SET machine_name = ?, ip_address = ? WHERE id = ?', (machine_name, ip_address, id))
            conn.commit()
        return redirect(url_for('index'))

    conn.close()
    return render_template('index.html', ip_records=ip_records)

@app.route('/ip_records', methods=['GET'])
def ip_records():
    conn = get_db_connection()
    ip_records = conn.execute('SELECT * FROM ip_records').fetchall()
    conn.close()
    return render_template('ip_records.html', ip_records=ip_records)

@app.route('/export', methods=['GET'])
def export_records():
    conn = get_db_connection()
    ip_records = conn.execute('SELECT * FROM ip_records').fetchall()
    conn.close()

    # Convert to DataFrame
    df = pd.DataFrame(ip_records, columns=['id', 'machine_name', 'ip_address'])

    # Create BytesIO object to store Excel file
    output = io.BytesIO()

   

    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='IP Records')
    output.seek(0)

    # Return Excel file as response
    return send_file(output, download_name='ip_records.xlsx', as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
