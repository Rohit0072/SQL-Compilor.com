from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def get_tables():
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    conn.close()
    return [table[0] for table in tables]

def execute_sql(command):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    try:
        cursor.execute(command)
        conn.commit()
        if command.strip().upper().startswith('SELECT'):
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            result = {"columns": columns, "rows": rows}
        else:
            result = {"columns": [], "rows": []}
        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "error": str(e)}
    finally:
        conn.close()

@app.route('/')
def index():
    tables = get_tables()
    return render_template('index.html', tables=tables)

@app.route('/execute', methods=['POST'])
def execute():
    command = request.form['command']
    response = execute_sql(command)
    return jsonify(response)

@app.route('/tables', methods=['GET'])
def tables():
    tables = get_tables()
    return jsonify({"tables": tables})

if __name__ == '__main__':
    app.run(debug=True)
