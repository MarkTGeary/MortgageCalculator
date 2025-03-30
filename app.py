from flask import Flask, request, jsonify, render_template_string, send_file
from flask_cors import CORS
import sqlite3


app = Flask(__name__)
CORS(app)


# HTML for table
TABLE_TEMPLATE = '''
<html>
<head>
    <title>Database Entries</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #4CAF50;
            text-align: center;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background-color: white;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Mortgage Details Based On User Data</h1>
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Income</th>
                    <th>Location(s)</th>
                    <th>Flexibility</th>
                    <th>Year</th>
                    <th>Down Payment</th>
                    <th>Mortgage Length</th>
                    <th>Monthly Payment</th>
                    <th>Within Budget?</th>
                    <th>Approved by Bank?</th>
                </tr>
            </thead>
            <tbody>
                {% for row in data %}
                <tr>
                    <td>{{ row[0] }}</td>
                    <td>€{{ row[1] }}</td>
                    <td>{{ row[2] }}</td>
                    <td>{{ row[3] }}</td>
                    <td>{{ row[4] }}</td>
                    <td>€{{ row[5] }}</td>
                    <td>{{ row[6] }} years</td>
                    <td>€{{ row[7] }}</td>
                    <td>{{ row[8] }}</td>
                    <td>{{ row[9] }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    <div style="text-align: center; margin-top: 20px;">
        <a href="javascript:history.back()">
        <button style="padding: 10px 20px; font-size: 16px; cursor: pointer;">Return to Mortgage Analysation</button>
        </a>
    </div>


</body>
</html>
'''
# Create Table if it doesn't already exist
def init_db():
    with sqlite3.connect('data.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS data 
                          (Name TEXT,
                           income INTEGER,
                           locations TEXT,
                           flexibility TEXT,
                           year INTEGER,
                           downPayment INTEGER, 
                           mortgageLength INTEGER,
                           monthlyPayment REAL,
                           approval TEXT,
                           Budget2 TEXT)''')
        conn.commit()
# Get Variables from Javascript
@app.route('/form', methods=['POST'])
def data():
    data = request.get_json()

    Name = data['name']
    income = data['income']
    locations = data['locations']
    flexibility = data['flexibility']
    year = data['year']
    downPayment = data['downPayment']
    mortgageLength = data['mortgageLength']
    monthlyPayment = data['monthlyPayment']
    approval = data['approval']
    Budget2 = data['Budget2']
    
    
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    
    # Insert Data into the table
    cursor.execute("""INSERT INTO data 
                     (Name, income, locations, flexibility, year, downPayment, mortgageLength, monthlyPayment, approval, Budget2)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                     (Name, income, locations, flexibility, year, downPayment, mortgageLength, monthlyPayment, approval, Budget2))
    
    conn.commit()
    conn.close()
    
    return "Data added successfully"
# View the Database
@app.route('/view_db', methods=['GET'])
def view_db():
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM data")
    rows = cursor.fetchall()
    
    conn.close()
    
    return render_template_string(TABLE_TEMPLATE, data=rows)

#Work with the mortgageAdvice file
@app.route('/mortgageAdvice.html')
def mortgage_advice_page():
    return send_file('mortgageAdvice.html')




if __name__ == '__main__':
    init_db()
    app.run(debug=True)