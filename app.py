from flask import Flask, g, render_template 
import sqlite3
from flask import g


app = Flask(__name__)

DATABASE = 'database_cars.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    cursor = get_db().cursor()
    sql = '''
SELECT Manufacturer.name, model, year, kms, price, type FROM cars
JOIN Transmission
ON Cars.transmission = Transmission.id
JOIN Manufacturer
ON Cars.manufacturer_id = Manufacturer.id
ORDER BY Manufacturer.name, model
'''
    cursor.execute(sql)
    results = cursor.fetchall()
    return render_template ("cars.html" , cars=results)

if __name__ == "__main__":
    app.run(debug=True)
