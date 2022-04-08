
import null
from flask import Flask, request, render_template, make_response
from flask_cors import CORS, cross_origin
import mysql.connector

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

hostName = "0.0.0.0"
serverPort = 8080
db = null;

query1 = "select * from zugangsdaten"
query2 = "insert into zugangsdaten values (%s,%s,%s)"
writeIntQuery = "insert into integers (integerNumber) values (%s)"
dbName = "sicherheit"


@app.route('/register/', methods=["POST"])
def gfg():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        file = open('server.log', 'a')
        file.write("Name: " + name + "Password: " + password)
        file.close()
        writeInDatabase((666,name,password))
        return "OK"

@app.route('/integer/', methods=["POST"])
@cross_origin()
def intToDB():
    if request.method == "POST":
        integer = request.form.get("integer")
        return make_response(writeIntToDatabase((integer,)))

@app.route('/', methods=["GET"])
def get():
    if request.method == "GET":
        return render_template("index.html")

def initiateDatabaseConnection():
    return mysql.connector.connect(
        host="localhost", user="root",
        password="IT-Sicherheit_Lab", database=dbName)

#help function to ensure we got connection to the database
def printTableFromDatabase():

    cursor = db.cursor()
    cursor.execute(query1)
    table = cursor.fetchall()
    for attr in table:
        print(attr)

#writes an i, name and password in a table specified in "query2" in the database
def writeInDatabase(data):
    cursor = db.cursor()
    cursor.execute(query2, data)
    db.commit()

#writes an integer form the form to the table integers in the database
def writeIntToDatabase(data):
    try:
        cursor = db.cursor()
        cursor.execute(writeIntQuery, data)
        db.commit()
        data = {'success' : 'true'}
        return (data, 200)
    except Exception as e:
        print(e)
        data = {'error' : str(e)}
        return (data, 422)

if __name__ == '__main__':
    db = initiateDatabaseConnection();
    printTableFromDatabase()
    app.run(host=hostName, ssl_context=('/etc/letsencrypt/live/itsicherheit.ddnss.de/fullchain.pem', '/etc/letsencrypt/live/itsicherheit.ddnss.de/privkey.pem'))


