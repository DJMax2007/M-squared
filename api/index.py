from flask import Flask, render_template, request
import os

app = Flask(__name__, 
            template_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'templates'),  
            static_folder=os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'static'))

@app.route('/')
def home():
    return render_template('feedback.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        # get the name, email, .......
    
    # save to databse
    # whatever with the form data

    # if name and email: return "name and email"
    print(f"Received name: {name}")
    return f" {name} Feedback submitted successfully123!"

if __name__ == '__main__':
    app.run(debug=True)
