from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import os
import smtplib
import cloudinary
import cloudinary.uploader
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

# cloud details for files
CLOUD_NAME = os.getenv("CLOUD_NAME")
CLOUD_KEY = os.getenv("CLOUD_KEY")
CLOUD_SECRET = os.getenv("CLOUD_SECRET")

app = Flask(__name__, 
            template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'templates'),  
            static_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'static'))

app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password}@{cluster}/{database}?retryWrites=true&w=majority"
mongo = PyMongo(app)

print(EMAIL_PASS, EMAIL_USER, EMAIL_USER2)

# Global Cloudinary configuration
cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=CLOUD_KEY,
    api_secret=CLOUD_SECRET
)

def send_email_notif(name, email, phone, issue, description, file_url=None):
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
File Link: {file_url if file_url else 'No file uploaded'}         

""")
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_USER, EMAIL_PASS)
        smtp.send_message(msg)
    
def handle_file_upload(file):
    if not file or not file.filename:
        return None

    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()

    allowed_exts = ['.jpg', '.jpeg', '.png', '.gif', '.pdf']
    if ext not in allowed_exts:
        raise ValueError("Unsupported file type")

    file.seek(0, os.SEEK_END)
    size_mb = file.tell() / (1024 * 1024)
    file.seek(0)
    if size_mb > 10:
        raise ValueError(f"{filename} file too large (max 10MB)")

    resource_type = "raw" if ext == '.pdf' else "image"

    upload_result = cloudinary.uploader.upload(
        file,
        resource_type=resource_type,
        type="upload",
        filename=filename
    )
    return upload_result.get("secure_url") or upload_result.get("url")

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
        file = request.files.get('upload')

        # adding the "+" sign for storage purpose
        if phone != '':
            phone = '+' + phone

        # TODO: deal with file uploads

        file_url = None
        try:
            file_url = handle_file_upload(file)
        except Exception as e:
            return render_template("errorpage.html", error_message=str(e)), 400

    
    # Email notification
        try:
            # save to database
            mongo.db.users.insert_one({
                'name': name,
                'email': email,
                'phone': phone,
                'issue': issue,
                'description':description,
                'file': file_url
            })
            # Email notification
            send_email_notif(name, email, phone, issue, description, file_url)
        except Exception as e:
            print(f"Error saving to database or sending email: {e}")
            return "Something went wrong", 500

    print(f"Received name: {name}")
    print(cloudinary.config().cloud_name)
    print(file_url)
    
    return render_template("success.html", name=name)

if __name__ == '__main__':
    app.run(debug=True)
