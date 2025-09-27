from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ----------------- Models -----------------
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(50))  # Add this line
    year = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default='available')
    borrows = db.relationship('Borrow', backref='book', lazy=True)

class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrow_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)

# ------------------------------------------


# ------------------ DATABASE INIT ------------------
with app.app_context():
    db.create_all()  # Creates tables if not exists

# ------------------ ROUTES ------------------
@app.route('/')
def home():
    books = Book.query.all()
    borrows = Borrow.query.all()
    return render_template('index.html', books=books, borrows=borrows)


# --------------- ADMIN ROUTES ----------------
@app.route('/admin/add_book', methods=['POST'])
def add_book():
    data = request.form
    new_book = Book(
        title=data['title'],
        author=data['author'],
        genre=data.get('genre', ''),
        year=int(data.get('year', 0))
    )
    db.session.add(new_book)
    db.session.commit()
    return redirect('/')

@app.route('/admin/delete_book/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect('/')

# ---------------- STUDENT ROUTES ----------------
@app.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book_form(book_id):
    book = Book.query.get_or_404(book_id)
    student_name = request.form['student_name']

    borrow_date = datetime.now()
    due_date = borrow_date + timedelta(days=7)  # Set due date 7 days later

    borrow_record = Borrow(
        student_name=student_name,
        book_id=book.id,
        borrow_date=borrow_date,
        due_date=due_date  # Pass the due date
    )

    book.status = 'borrowed'
    db.session.add(borrow_record)
    db.session.commit()

    return redirect(url_for('home'))



@app.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    student_name = request.form.get('student_name')
    book = Book.query.get_or_404(book_id)

    # Set borrow date and due date (e.g., 14 days later)
    borrow_date = datetime.utcnow()
    due_date = borrow_date + timedelta(days=14)

    borrow_record = Borrow(
        student_name=student_name,
        book_id=book.id,
        borrow_date=borrow_date,
        due_date=due_date
    )

    db.session.add(borrow_record)
    db.session.commit()

    return redirect(url_for('home'))



# ------- API ROUTES --------

@app.route('/api/borrow/<int:book_id>/<student_name>', methods=['GET'])
def borrow_book_api(book_id, student_name):
    book = Book.query.get_or_404(book_id)
    if book.status == 'available':
        book.status = 'borrowed'
        borrow_record = Borrow(student_name=student_name, book_ref=book)
        db.session.add(borrow_record)
        db.session.commit()
        return {"message": f"{student_name} borrowed {book.title}"}
    else:
        return {"message": "Book already borrowed"}, 400


@app.route('/return/<int:borrow_id>', methods=['POST'])
def return_book_api(borrow_id):
    borrow = Borrow.query.get(borrow_id)
    if borrow:
        # Mark book as available
        borrow.book.status = 'available'
        # Delete the borrow record
        db.session.delete(borrow)
        db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)