import pyotp
import qrcode as qrcode
from flask import Flask, request, render_template, make_response, redirect, jsonify
from flask_cors import CORS, cross_origin
import mysql.connector
from pyotp import totp

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

hostName = "0.0.0.0"
serverPort = 8080
db = None;

query1 = "select * from zugangsdaten"
query2 = "insert into zugangsdaten values (%s,%s,%s,%s)"
writeIntQuery = "insert into integers (integerNumber) values (%s)"
dbName = "sicherheit"


@app.route('/register/', methods=["POST", "GET"])
def gfg():
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        saveDataToTextFile(name)
        saveDataToTextFile(password)
        secretKey = pyotp.random_base32(32)
        writeInDatabase((666,name,password,secretKey))
        generateQrCode(secretKey, name)
        return render_template("verifyQr.html", qrcode = "../" + qrCodePath, name = name, password = password)
    if request.method == "GET":
        return render_template("register.html")

qrCodeFileName = "qrCode.jpg"
staticLocation = "static"
qrCodePath = staticLocation + "/" + qrCodeFileName

def generateQrCode(secretKey, name):
    totp = pyotp.totp.TOTP(secretKey)
    qrCode = qrcode.make(totp.provisioning_uri(name=name, issuer_name='Secure App'))
    qrCode.save(qrCodePath)

@app.route('/login/', methods=["GET", "POST"])
def loginRedirect():
    if request.method == "GET":
        return redirect('/')
    if request.method == "POST":
        userOtp = request.form.get("code")
        name = request.form.get("name")
        password = request.form.get("password")
        return loginWithOtp(name, password, userOtp)

@app.route('/', methods=["GET"])
def get():
    if request.method == "GET":
        return render_template("login.html")

@app.route('/verifyQr/', methods=["POST"])
def getVerifyQr():
    if request.method == "POST":
        userOtp = request.form.get("code")
        name = request.form.get("name")
        password = request.form.get("password")
        return loginWithOtp(name, password, userOtp)

def loginWithOtp(name, password, otp):
        cursor = db.cursor()
        userQuery = "select * from zugangsdaten where name = (%s) and password = (%s)"
        cursor.execute(userQuery, (name, password))
        try:
            table = cursor.fetchone()
        finally:
            print(table)
            if not table is None and table[1] == name and table[2] == password:
                totp = pyotp.totp.TOTP(table[3])
                if otp == totp.now():
                    print("success")
                    return render_template("loggedIn.html")
                else:
                    print("wrong code")
                    return make_response(
                        jsonify(
                            {"message": "wrong Code", "severity": "light"}
                        ),
                        401,)
                return render_template("loggedIn.html")
            else:
                return make_response(
                    jsonify(
                            {"message": "wrong Code", "severity": "light"}
                    ),
                    401,)

def saveDataToTextFile(str):
    file = open('data.txt', 'a')
    file.write('\n' + str)
    file.close

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
    try:
        cursor = db.cursor(buffered=True)
        cursor.execute(query2, data)
        result = "true";
        try:
            result = cursor.fetchall()
        finally:
            db.commit()
            data = {'success' : str(result)}
            return (data, 200)
    except Exception as e:
        print(e)
        data = {'error' : str(e)}
        return(data, 422)

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
    #printTableFromDatabase()
    app.run(host=hostName, ssl_context=('/etc/letsencrypt/live/itsicherheit.ddnss.de/fullchain.pem', '/etc/letsencrypt/live/itsicherheit.ddnss.de/privkey.pem'))


