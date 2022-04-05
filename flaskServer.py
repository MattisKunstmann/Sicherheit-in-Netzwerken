import null
from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

hostName = "localhost"
serverPort = 8080
db = null;

query1 = "select * from zugangsdaten"
query2 = "insert into zugangsdaten values (%s,%s,%s)"
dbName = "sicherheit"


@app.route('/', methods=["POST"])
def gfg():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        writeInDatabase((666,name,password))
        return "OK"


@app.route('/', methods=["GET"])
def get():
    if request.method == "GET":
        return render_template("index.html")

def initiateDatabaseConnection():
    return mysql.connector.connect(
        host="localhost", user="root",
        password="", database=dbName)

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
    table = cursor.fetchall()
    for attr in table:
        print(attr)



if __name__ == '__main__':
    db = initiateDatabaseConnection();
    printTableFromDatabase()
    app.run()


