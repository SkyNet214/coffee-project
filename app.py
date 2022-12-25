import datetime
from flask import Flask, request, render_template, url_for
import json, smtplib, ssl, time
from email.mime.text import MIMEText


app = Flask(__name__)

with open("valid_codes.json") as f:
    valid_codes = json.load(f)
immortal_id = "2357" # id for debugging

sender_email = "remote.coffee.website@gmail.com"
receiver_email = "niklas20066@gmail.com"
password = "3M@w/%7v]m~g.B|]:}u&5R-.D;P{=>&N"
app_password = "qcfipoftzfmkiqsl"
port = 587


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    code = request.form["code"]
    context = request.form["context"]
    
    if code in valid_codes["codes"]:
        if code != immortal_id:
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            msg = MIMEText(f"New coffee request received!\n\n {date_time} \n\n {context}")
            msg["Subject"] = "New coffee request received!"
            msg["From"] = sender_email
            msg["To"] = receiver_email
            context = ssl.create_default_context()
            server = smtplib.SMTP("smtp.gmail.com", port)
            server.starttls()
            server.login(sender_email, app_password)
            print(server.sendmail(sender_email, receiver_email, msg.as_string()))
            server.close()
            valid_codes["codes"].remove(code)
            with open("valid_codes.json", "w") as f:
                json.dump(valid_codes, f)
        
        return {"success": True}

    else:
        return {"success": False}
    

app.run(host="0.0.0.0", port=80)

