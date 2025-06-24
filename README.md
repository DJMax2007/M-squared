# 🛠️ Issue Submission App

A lightweight Flask web app that allows users to submit support issues, upload files, and automatically notify you via email. All submissions are stored in MongoDB.

---

## 🚀 Features

- 📄 Form with fields:
  - Name
  - Email
  - Phone (optional, validated)
  - Issue Type (dropdown)
  - Description
  - File Upload (PDF, JPG, PNG)
- ☁️ Stores data in MongoDB Atlas
- 📧 Sends email notifications to admin via SMTP

---

## 🗂️ Project Picture
<img width="436" alt="Screenshot 2025-06-23 at 6 47 41 PM" src="https://github.com/user-attachments/assets/a985cafb-fa03-4d30-bc0f-0b964bf1e2b5" />


---

## ⚙️ Setup

### 1. Clone & Install

```bash
git clone https://github.com/DJMax2007/M-squared.git
cd M-squared
pip install -r requirements.txt
```
### 2. Configure Environment
Create a `.env` file in the [`api`](api/) directory:

```env
# MongoDB
MONGO_USERNAME=your_mongo_user
MONGO_PASSWORD=your_mongo_pass
MONGO_CLUSTER=cluster0.abcde.mongodb.net
MONGO_DB=yourdbname

# Email (Gmail)
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password
```
> ⚠️ Use Gmail App Passwords if using Gmail.

### 3. Run App
#### Option 1. 
`python api/index.py` on Windows
`python3 api/index.py` on MacOS/Linux

#### Option 2. 

##### On Windows (CMD):
```c
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```

##### On Windows (Powershell)
```powershell
$env:FLASK_APP = "app.py"
$env:FLASK_ENV = "development"
flask run
```

##### On MacOS/Linux
```bash
export FLASK_APP=app.py
export FLASK_ENV=development  # Enables debug mode (auto-reload)
flask run
```

### 4. Visit Link
Visit: http://127.0.0.1:5000/

