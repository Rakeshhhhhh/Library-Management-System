from . import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)
    average_rating = db.Column(db.Float, nullable=True)
    isbn = db.Column(db.String(10), nullable=False)
    isbn13 = db.Column(db.String(13), nullable=False)
    language_code = db.Column(db.String(3), nullable=False)
    num_pages = db.Column(db.Integer, nullable=False)
    ratings_count = db.Column(db.Integer, nullable=False)
    text_reviews_count = db.Column(db.Integer, nullable=False)
    publication_date = db.Column(db.Date, nullable=False)
    publisher = db.Column(db.String(255), nullable=False)
    total_quantity = db.Column(db.Integer, nullable=False)
    available_quantity = db.Column(db.Integer, nullable=False)
    rented_count = db.Column(db.Integer, nullable=False)

    # Relationship with transactions
    transactions = db.relationship('Transaction', backref='book', lazy=True)

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"


class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    outstanding_debt = db.Column(db.Float, nullable=False)
    amount_spent = db.Column(db.Float, nullable=False)

    # Relationship with transactions
    transactions = db.relationship('Transaction', backref='member', lazy=True)

    def __repr__(self):
        return f"<Member {self.name} ({self.email})>"


class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    member_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False)
    per_day_fee = db.Column(db.Float, nullable=False)
    borrowed_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    returned_on = db.Column(db.DateTime, nullable=True)
    total_charge = db.Column(db.Float, nullable=True)
    amount_paid = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Transaction {self.id}: Book {self.book_id} borrowed by Member {self.member_id}>"