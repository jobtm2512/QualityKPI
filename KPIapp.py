from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "your_secret_key"

# MySQL Configuration
db = mysql.connector.connect(host="localhost", user="root", passwd="jobtmmysql2512", db="quality_management")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_quality_indicator', methods=['GET', 'POST'])
def add_quality_indicator():
    cursor = db.cursor()

    # Fetch the latest indicator_id, ensure it starts with 'QI'
    cursor.execute("SELECT indicator_id FROM quality_indicators WHERE indicator_id LIKE 'QI%' ORDER BY id DESC LIMIT 1")
    last_indicator = cursor.fetchone()
    
    # Generate the next indicator_id (e.g., QI1, QI2, QI3...)
    if last_indicator:
        last_number = int(last_indicator[0][2:])  # Extract the number after 'QI'
        next_indicator_id = f"QI{last_number + 1}"
    else:
        next_indicator_id = "QI1"  # If no indicators yet, start with QI1

    if request.method == 'POST':
        indicator_name = request.form['indicator_name']
        numerator = request.form['numerator']
        denominator = request.form['denominator']
        factor = request.form['factor']
        frequency = request.form['frequency']
        benchmark = request.form['benchmark']

        # Insert the new quality indicator
        cursor.execute("""
            INSERT INTO quality_indicators (indicator_id, indicator_name, numerator, denominator, factor, frequency, benchmark)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (next_indicator_id, indicator_name, numerator, denominator, factor, frequency, benchmark))
        db.commit()
        
        flash("Quality Indicator Added Successfully")
        return redirect(url_for('index'))

    return render_template('add_quality_indicator.html', next_indicator_id=next_indicator_id)


@app.route('/add_division_dept', methods=['GET', 'POST'])
def add_division_dept():
    if request.method == 'POST':
        cursor = db.cursor()
        division_name = request.form['division_name']
        department_name = request.form['department_name']
        sub_department_name = request.form['sub_department_name']
        
        # Insert division, department, and sub-department
        cursor.execute("INSERT INTO Division (division_name) VALUES (%s)", [division_name])
        division_id = cursor.lastrowid
        cursor.execute("INSERT INTO Department (department_name, division_id) VALUES (%s, %s)", [department_name, division_id])
        department_id = cursor.lastrowid
        cursor.execute("INSERT INTO Sub_department (sub_department_name, department_id) VALUES (%s, %s)", [sub_department_name, department_id])
        db.commit()
        flash("Division, Department, and Sub-department Added Successfully")
        return redirect(url_for('index'))
    return render_template('add_division_dept.html')

@app.route('/tag_quality_indicator', methods=['GET', 'POST'])
def tag_quality_indicator():
    cursor = db.cursor()
    
    # Fetch all quality indicators
    cursor.execute("SELECT indicator_id, indicator_name FROM quality_indicators")
    quality_indicators = cursor.fetchall()

    # Fetch all departments
    cursor.execute("SELECT department_id, department_name FROM Department")
    departments = cursor.fetchall()

    # Fetch all sub-departments
    cursor.execute("SELECT sub_department_id, sub_department_name FROM Sub_department")
    sub_departments = cursor.fetchall()

    if request.method == 'POST':
        quality_indicator_id = request.form['quality_indicator_id']
        department_id = request.form['department_id']
        sub_department_id = request.form.get('sub_department_id')  # Optional

        # Insert data into the quality_indicator_tags table
        cursor.execute("""
            INSERT INTO quality_indicator_tags (quality_indicator_id, department_id, sub_department_id)
            VALUES (%s, %s, %s)
        """, (quality_indicator_id, department_id, sub_department_id))
        db.commit()

        flash("Quality Indicator Tagged Successfully")
        return redirect(url_for('index'))
    
    return render_template('tag_quality_indicator.html', 
                            quality_indicators=quality_indicators, 
                            departments=departments, 
                            sub_departments=sub_departments)


if __name__ == '__main__':
    app.run(debug=True)
