

# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import requests
import null as null
import cgi



hostName = "localhost"
serverPort = 8080
db = null;

query1 = "select * from zugangsdaten"
query2 = "insert into zugangsdaten values (%s,%s,%s)"
# query3 = """INSERT INTO `zugangsdaten`(`id`, `name`, `password`) VALUES (55,'[value-2]','[value-3]')"""
dbName = "sicherheit"


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        content = open('index.html').read()
        self.wfile.write(content.encode())

    def do_POST(self):

        #if self.path == '/success':
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            # pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
            #
            # if ctype == 'multipart/form-data':
            fields = cgi.parse(self.rfile)
            name = fields.get("name")[0]
            password = fields.get("password")[0]
            print(name + " " + password)
            writeInDatabase((123, name, password))
            # else:
            #     print("afjhdkfjh")

        #else:
        #    print("bullshit")

        # content_length = int(self.headers['Content-Length'])
        # post_data = self.rfile.read(content_length)




def initiateDatabaseConnection():
    return mysql.connector.connect(
        host="localhost", user="root",
        password="", database=dbName)


def printTableFromDatabase():
    cursor = db.cursor()
    cursor.execute(query1)

    table = cursor.fetchall()
    for attr in table:
        print(attr)


def writeInDatabase(data):
    print("writing in db")
    cursor = db.cursor()
    cursor.execute(query2, (3, 'bla', 'password'))
    db.commit()
    table = cursor.fetchall()
    for attr in table:
        print(attr)


if __name__ == "__main__":

    db = initiateDatabaseConnection();
    printTableFromDatabase()

    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
