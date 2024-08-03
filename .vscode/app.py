
from flask import Flask, request, render_template
import mysql.connector as ms

app = Flask(__name__)

def get_db_connection():
    try:
        con = ms.connect(host='localhost', user='root', password='Vedha@2006', database='college')
        return con
    except ms.Error as err:
        print(f"Error: {err}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            cutoff = float(request.form['cutoff'])
            course = request.form['course']
        except ValueError:
            return render_template('cut-off.html', error="Invalid cutoff value")

        return render_template('eligibility.html', cutoff=cutoff, course=course)
    
    return render_template('cut-off.html')

@app.route('/table', methods=['GET'])
def result():
    try:
        cutoff = float(request.args.get('cutoff', ''))
        course = request.args.get('course', '')
    except ValueError:
        return render_template('cut-off.html', error="Invalid cutoff value")

    con = get_db_connection()
    if not con:
        return render_template('cut-off.html', error="Database connection failed")

    cursor = con.cursor()

    if cutoff < 150:
        q1 = "SELECT * FROM deemed"
        cursor.execute(q1)
        data = cursor.fetchall()
        cursor.close()
        con.close()
        return render_template('table.html', data=data, eligible=False)
    else:
        q2 = "SELECT CODE, NAME FROM counselling WHERE {} <= {}".format(course, cutoff)
        cursor.execute(q2)
        data = cursor.fetchall()
        cursor.close()
        con.close()
        return render_template('table.html', data=data, eligible=True)

if __name__ == '__main__':
    app.run(debug=True)
