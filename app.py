from datetime import date
import datetime
from email import message
from flask import Flask, request, render_template, url_for
import json, smtplib, ssl, time

from werkzeug.datastructures import ContentRange

app = Flask(__name__)

immortal_id = "2357" # id for debugging

sender_email = "remote.coffee.website@gmail.com"
receiver_email = "niklas20066@gmail.com"
password = "3M@w/%7v]m~g.B|]:}u&5R-.D;P{=>&N"
port = 465
context = ssl.create_default_context()
message_template = lambda remarks, time: f"""\
Subject: New coffee request received

request time: {time}

remarks: {remarks}

"""

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
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login(sender_email, password)
                print(server.sendmail(sender_email, receiver_email, message_template(body["remarks"], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))))
        id_list = json.loads(open("id_list.json", "r").read())
        for i in id_list["id_list"]["ids"]:
            if i["id"] == body["id"] and i["id"] != immortal_id:
                i["valid"] = body["valid"]
        open("id_list.json", "w").write(json.dumps(id_list))
        return json.dumps({"success": True})


app.run(host="0.0.0.0")