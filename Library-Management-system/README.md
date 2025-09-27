#  Library Management System (Books + Borrowing)

##  Team Details
- Name: Shrimali Bhargav Narendrabhai
- Roll No: 23DCS125
- Course: B.Tech CSE (5th Sem)

---

##  Project Description
A simple **Library Management System** built with Flask + SQLite.  
It allows:
- Admin to add, update, and remove books.
- Students to borrow and return books.
- API endpoints for managing borrowing & returning.
- (Optional) Track due dates & overdue fines.

---

##  Features
- Admin Panel: Add / Edit / Delete books.
- Student Panel: Borrow / Return books.
- API Endpoints for integration.
- SQLite lightweight database.

---

##  Tech Stack
- Python (Flask)
- SQLite
- HTML, CSS, Bootstrap
- REST API (Flask-Restful)

---

##  Setup Instructions
1. Clone this repo:
   ```bash
   git clone https://github.com/your-username/Library-Management-System.git
   cd Library-Management-System

2. Create a virtual environment (recommended)
python -m venv venv


Activate the virtual environment:

Windows:

venv\Scripts\activate


Linux/Mac:

source venv/bin/activate

3. Install dependencies
pip install -r requirements.txt


If you don't have a requirements.txt, install manually:

pip install flask sqlalchemy

4. Initialize the database

Run the following Python commands in the project folder:

from app import db, app
with app.app_context():
    db.create_all()


This will create the library.db SQLite database and necessary tables.

5. Run the application
python app.py


By default, the Flask app will run at:

http://127.0.0.1:5000/

6. Using the Application

Open the above URL in your browser.

Admin can manage books via the interface.

Students can borrow and return books.

All borrow records and due dates are visible on the home page.
