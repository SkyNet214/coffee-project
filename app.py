import json, smtplib, ssl, datetime, os, mysql.connector
from flask import Flask, request, render_template
from email.mime.text import MIMEText
from dotenv import load_dotenv
from mysql.connector import Error


load_dotenv()
app = Flask(__name__)

sender_email = "remote.coffee.website@gmail.com"
receiver_email = "niklas20066@gmail.com"
app_password = os.getenv("APP_PASSWORD")
port = 587

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: {err}")

    return connection

connection = create_db_connection("localhost", os.getenv("DB_USERNAME"), os.getenv("DB_PASSWORD"), "coffee")

def query(query: str) -> tuple:
    '''Execute query, return result and handle errors'''
    result = None
    if connection != None:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchone()
            connection.commit()
        except Error as err:
            print(f"Error: {err}")
    else:
        print("Error: No connection to DBMS server")
    return result


def get_user_balance(username: str) -> int:
    '''Query and return user balance in database and return -1 if user doesn't exist or no connection is available'''
    result = query(f"SELECT balance FROM users WHERE username='{username}'")
    if result != None:
        return result[0]
    return -1

def update_user_balance(username: str, value: int):
    '''Perform a query to set the users balance to value'''
    query(f"UPDATE users SET balance={value} WHERE username='{username}';")
    
def send_notification_email(username: str, context: str):
    date_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    msg = MIMEText(f"New coffee request received from {username}!\n\n {date_time} \n\n {context}")
    msg["Subject"] = "New coffee request received!"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP("smtp.gmail.com", port)
        server.starttls()
        server.login(sender_email, app_password)
        print(server.sendmail(sender_email, receiver_email, msg.as_string()))
        server.close()
        return True
    except smtplib.SMTPConnectError as e:
        print(f"Error: {e}")
    except:
        print(f"Error: Couldn't send email")
    return False

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/checkname", methods=["POST"])
def check():
    username = request.get_data(as_text=True)
    balance = get_user_balance(username)
    if balance != -1:
        return {"username": username, "count": balance} 
    return {}

@app.route("/submit", methods=["POST"])
def submit():
    username = request.form["username"]
    context = request.form["context"]
    balance = get_user_balance(username)
    
    if balance != -1:
        if balance == 0:
            return {"username": username, "count": -1}
        else:
            new_balance = balance - 1
            update_user_balance(username, new_balance)
            send_notification_email(username, context)
            return {"username": username, "count": balance}
    return {}
    
if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=80)
    except KeyboardInterrupt:
        connection.close()