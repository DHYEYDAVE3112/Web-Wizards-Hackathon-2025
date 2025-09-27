from flask import Blueprint, jsonify, request
from models import db, Book, Borrow
import datetime

api = Blueprint('api', __name__)

# Get all books
@api.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    result = [{"id": b.id, "title": b.title, "author": b.author, "available": b.available} for b in books]
    return jsonify(result)

# Add new book (Admin)
@api.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    book = Book(title=data['title'], author=data['author'], available=True)
    db.session.add(book)
    db.session.commit()
    return jsonify({"message": "Book added successfully"}), 201

# Update book details
@api.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    data = request.get_json()
    book.title = data.get('title', book.title)
    book.author = data.get('author', book.author)
    db.session.commit()
    return jsonify({"message": "Book updated successfully"})

# Delete book
@api.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted successfully"})

# Borrow book
@api.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    book = Book.query.get(book_id)
    if not book or not book.available:
        return jsonify({"error": "Book not available"}), 400
    book.available = False
    borrow = Borrow(book_id=book_id, borrow_date=datetime.date.today())
    db.session.add(borrow)
    db.session.commit()
    return jsonify({"message": "Book borrowed successfully"})

# Return book
@api.route('/return/<int:book_id>', methods=['POST'])
def return_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    borrow = Borrow.query.filter_by(book_id=book_id, return_date=None).first()
    if not borrow:
        return jsonify({"error": "This book was not borrowed"}), 400
    book.available = True
    borrow.return_date = datetime.date.today()
    db.session.commit()
    return jsonify({"message": "Book returned successfully"})
