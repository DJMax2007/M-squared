from flask import Flask, render_template, request
from flask_pymongo import PyMongo
import os

from dotenv import load_dotenv

load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER")
database = os.getenv("MONGO_DB")


app = Flask(__name__, 
            template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'templates'),  
            static_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'static'))

app.config["MONGO_URI"] = f"mongodb+srv://{username}:{password}@{cluster}/{database}?retryWrites=true&w=majority"
mongo = PyMongo(app)


@app.route('/')
def home():
    return render_template('feedback.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        mongo.db.users.insert_one({
            'name': name,
            'email': email,
            'phone': phone
        })
        # get the name, email, .......
    
    # save to databse
    # whatever with the form data

    # if name and email: return "name and email"
    print(f"Received name: {name}")
    return f" {name} Feedback submitted successfully123!"

if __name__ == '__main__':
    app.run(debug=True)
