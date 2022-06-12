import time

import pyotp
import qrcode as qrcode
from flask import Flask, request, render_template
import mysql.connector
from pyotp import totp

app = Flask(__name__)

hostName = "localhost"
serverPort = 8080
db = None;

query1 = "select * from zugangsdaten"
query2 = "insert into zugangsdaten values (%s,%s,%s)"
dbName = "sicherheit"


@app.route('/login', methods=["POST"])
def gfg():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        print(password+name)
        #writeInDatabase((666,name,password))
        return "OK"

@app.route('/register', methods=["POST"])
def gfg():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("passwordregister")
        # writeInDatabase((666,name,password))
        return "OK"

qrCodeFileName = "qrCode.png"
staticLocation = "static"
qrCodePath = staticLocation + "/" + qrCodeFileName

def generateQrCode():
    secretKey = pyotp.random_base32(32)
    totp = pyotp.totp.TOTP(secretKey)
    qrCode = qrcode.make(totp.provisioning_uri(name='alice@google.com', issuer_name='Secure App'))
    oneTimePassword = totp.now()
    qrCode.save(qrCodePath)

@app.route('/', methods=["GET"])
def get():
    if request.method == "GET":
        return render_template("index.html", qrcode = qrCodePath)

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
    #db = initiateDatabaseConnection();
    #printTableFromDatabase()


    # totp = pyotp.TOTP('base32secret3232')
    # totp.now()  # => '492039'
    #
    # # OTP verified for current time
    # totp.verify('492039')  # => True
    # time.sleep(30)
    # totp.verify('492039')  # => False


    app.run()


