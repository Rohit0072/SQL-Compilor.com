from flask import Flask, request, jsonify, render_template, url_for
import sqlite3
import os

app = Flask(__name__)

def execute_sql_command(command):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    try:
        cursor.execute(command)
        if command.strip().lower().startswith('select'):
            result = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in result]
        else:
            conn.commit()
            result = {'status': 'success'}
    except Exception as e:
        result = {'status': 'error', 'message': str(e)}
    finally:
        conn.close()
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute', methods=['POST'])
def execute():
    command = request.json['command']
    result = execute_sql_command(command)
    return jsonify(result=result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
