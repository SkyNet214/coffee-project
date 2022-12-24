from datetime import date
import datetime
from flask import Flask, request, render_template, url_for
import json, smtplib, ssl, time
from email.mime.text import MIMEText


app = Flask(__name__)

immortal_id = "2357" # id for debugging

sender_email = "remote.coffee.website@gmail.com"
receiver_email = "niklas20066@gmail.com"
password2 = "3M@w/%7v]m~g.B|]:}u&5R-.D;P{=>&N"
app_password = "qcfipoftzfmkiqsl"
port = 465
context = ssl.create_default_context()
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()
server.login(sender_email, app_password)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/idlist", methods=["GET", "POST"])
def idlist():
    if request.method == "GET":
        id = request.args["id"]
        id_list = json.loads(open("id_list.json", "r").read())["id_list"]["ids"]
        for i in id_list:
            if i["id"] == id:
                return i
        return {}
    elif request.method == "POST":
        body = request.json
        if body["valid"] == False and body["id"] != immortal_id:
            date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            remarks = body["remarks"]
            msg = MIMEText(f"New coffee request received!\n\n {date_time} \n\n {remarks}")
            msg["Subject"] = "New coffee request received!"
            msg["From"] = sender_email
            msg["To"] = receiver_email
            print(server.sendmail(sender_email, receiver_email, msg.as_string()))
        id_list = json.loads(open("id_list.json", "r").read())
        for i in id_list["id_list"]["ids"]:
            if i["id"] == body["id"] and i["id"] != immortal_id:
                i["valid"] = body["valid"]
        open("id_list.json", "w").write(json.dumps(id_list))
        return json.dumps({"success": True})

@app.route('/submit', methods=['POST'])
def submit():
    cid = int(request.form['couponid'])
    print(cid)
    extrawish = request.form['extrawishes']
    id_file = open("valid_ids.txt", "w+")
    valid_ids = id_file.readlines()
    if cid in [int(id) for id in valid_ids]:
        date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg = MIMEText(f"New coffee request received!\n\n {date_time} \n\n {extrawish}")
        msg["Subject"] = "New coffee request received!"
        msg["From"] = sender_email
        msg["To"] = receiver_email
        print(server.sendmail(sender_email, receiver_email, msg.as_string()))

        id_file.write("".join([line + "\n" for line in valid_ids if int(line) != cid]))
        id_file.close()
        return render_template("success.html")
    else:
        id_file.write("".join([line + "\n" for line in valid_ids]))
        id_file.close()
        return render_template("failure.html")

app.run(host="0.0.0.0")
server.quit()