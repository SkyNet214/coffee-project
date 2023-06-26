import datetime
from flask import Flask, request, render_template, url_for
import json, smtplib, ssl, time
from email.mime.text import MIMEText


app = Flask(__name__)

filename = "users.json"
admin = "Heisenberg" # user for debugging

sender_email = "remote.coffee.website@gmail.com"
receiver_email = "niklas20066@gmail.com"
password = "3M@w/%7v]m~g.B|]:}u&5R-.D;P{=>&N"
app_password = "qcfipoftzfmkiqsl"
port = 587

def read_file():
    with open(filename, "r") as f:
        return json.load(f)

def write_file(username, count):
    with open(filename, "w+") as f:
        db = json.load(f)
        if username in db.keys():
            db[username] = count
            json.dump(db, f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/checkname", methods=["POST"])
def check():
    username = request.get_data(as_text=True)
    db = read_file()
    if username in db.keys():
        return {"username": username, "count": db[username]} 
    return {}

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    context = request.form["context"]
    db = read_file()
    if username in db.keys():
        if username != admin:
            if db[username] <= 0:
                return {"username": username, "count": -1}
            else:
                date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                msg = MIMEText(f"New coffee request received from {username}!\n\n {date_time} \n\n {context}")
                msg["Subject"] = "New coffee request received!"
                msg["From"] = sender_email
                msg["To"] = receiver_email
                context = ssl.create_default_context()
                server = smtplib.SMTP("smtp.gmail.com", port)
                server.starttls()
                server.login(sender_email, app_password)
                print(server.sendmail(sender_email, receiver_email, msg.as_string()))
                server.close()
                db[username] = db[username] - 1
                write_file(username, db[username])
                return {"username": username, "count": db[username]}
        
        return {"username": username, "count": db[username]}
    return {}
    

app.run(host="0.0.0.0", port=80)

