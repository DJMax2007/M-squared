from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")
database = os.getenv("MONGO_DB")

# email details for smtplib
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_USER2 = os.getenv("EMAIL_USER2")
EMAIL_PASS = os.getenv("EMAIL_PASS")

app = Flask(__name__, 
            template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'templates'),  
            static_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'static'))

app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password}@{cluster}/{database}?retryWrites=true&w=majority"
mongo = PyMongo(app)

def send_email_notif(name, email, phone, issue, description):
    msg = EmailMessage()
    msg["Subject"] = f"WEB APP - New Issue: {issue}"
    msg["From"] = EMAIL_USER
    msg["To"] = ", ".join([EMAIL_USER,EMAIL_USER2, email])
    msg.set_content(f"""
New Issue Created:

Name: {name}
Email: {email}
Phone: {phone}
Issue Type: {issue}
Description:
{description}         

""")
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
    

@app.route('/')
def home():
    return render_template('feedback.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone', '').strip()
        issue = request.form.get('issue')
        description = request.form.get('description')

        # adding the "+" sign for storage purpose
        if phone != '':
            phone = '+' + phone


        # TODO: deal with file uploads

        # save to databse
        mongo.db.users.insert_one({
            'name': name,
            'email': email,
            'phone': phone,
            'issue': issue,
            'description':description
        })
    
    # Email notification
    send_email_notif(name, email, phone, issue, description)

    print(f"Received name: {name}")
    return f" Hi {name}, your feedback has been submitted!"

if __name__ == '__main__':
    app.run(debug=True)
