from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Book, db
from datetime import datetime
from wtforms import Form, StringField, FloatField, IntegerField, DateField, validators
import requests
import urllib.parse
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional

# Create a Blueprint for book routes
book_routes = Blueprint('book_routes', __name__)

# Define Add-Book-Form
class AddBook(Form):
    title = StringField('Title', [validators.Length(min=2, max=255)])
    author = StringField('Author(s)', [validators.Length(min=2, max=255)])
    average_rating = FloatField('Average Rating', [validators.NumberRange(min=0, max=5)])
    isbn = StringField('ISBN', [validators.Length(min=10, max=10)])
    isbn13 = StringField('ISBN13', [validators.Length(min=13, max=13)])
    language_code = StringField('Language', [validators.Length(min=1, max=3)])
    num_pages = IntegerField('No. of Pages', [validators.NumberRange(min=1)])
    ratings_count = IntegerField('No. of Ratings', [validators.NumberRange(min=0)])
    text_reviews_count = IntegerField('No. of Text Reviews', [validators.NumberRange(min=0)])
    publication_date = DateField('Publication Date', [validators.InputRequired()])
    publisher = StringField('Publisher', [validators.Length(min=2, max=255)])
    total_quantity = IntegerField('Total No. of Books', [validators.NumberRange(min=1)])

# List all books
@book_routes.route('/books')
def list_books():
    books = Book.query.all()
    return render_template('books.html', books=books)

# Add a new book
@book_routes.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = AddBook(request.form)
    if request.method == 'POST' and form.validate():
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            average_rating=form.average_rating.data,
            isbn=form.isbn.data,
            isbn13=form.isbn13.data,
            language_code=form.language_code.data,
            num_pages=form.num_pages.data,
            ratings_count=form.ratings_count.data,
            text_reviews_count=form.text_reviews_count.data,
            publication_date=form.publication_date.data,
            publisher=form.publisher.data,
            total_quantity=form.total_quantity.data,
            available_quantity=form.total_quantity.data,
            rented_count=0
        )
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('book_routes.list_books'))
    return render_template('add_book.html', form=form)

# View details of a book
@book_routes.route('/book/<int:id>')
def view_book(id):
    book = Book.query.get_or_404(id)
    return render_template('view_book_details.html', book=book)

# Edit a book
@book_routes.route('/edit_book/<int:id>', methods=['GET', 'POST'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    form = AddBook(request.form, obj=book)
    if request.method == 'POST' and form.validate():
        form.populate_obj(book)
        db.session.commit()
        flash('Book updated successfully!', 'success')
        return redirect(url_for('book_routes.list_books'))
    return render_template('edit_book.html', form=form, book=book)

# Delete a book
@book_routes.route('/delete_book/<int:id>', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('book_routes.list_books'))

