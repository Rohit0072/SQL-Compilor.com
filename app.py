from flask import Flask, render_template, request, jsonify
import sqlite3

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

app = Flask(__name__)

DATABASE = 'example.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tables', methods=['GET'])
def get_tables():
    conn = get_db_connection()
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [row['name'] for row in cursor.fetchall()]
    conn.close()
    return jsonify({"tables": tables})

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(command)
        conn.commit()
        if command.strip().upper().startswith("SELECT"):
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            result = {
                "columns": columns,
                "rows": [list(row) for row in rows]
            }
            return jsonify({"status": "success", "result": result})
        else:
            return jsonify({"status": "success", "result": {"columns": [], "rows": []}})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})
    finally:
        conn.close()

@app.route('/delete_table', methods=['POST'])
def delete_table():
    table_name = request.form['table_name']
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"DROP TABLE {table_name}")
        conn.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})
    finally:
        conn.close()

@app.route('/update_table', methods=['POST'])
def update_table():
    table_name = request.form['table_name']
    set_clause = request.form['set_clause']
    where_clause = request.form['where_clause']
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}")
        conn.commit()
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)
