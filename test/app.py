from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/check", methods=["GET"])
def checkid():
    id = request.args["id"]
    f = open("C:\\Users\\nikla\\Desktop\\web-dev\\test\\id_list.txt", "r")
    id_list = f.read().splitlines()
    if id in id_list:
        return "true"
    else:
        return "false"

if __name__ == "__main__":
    app.run()