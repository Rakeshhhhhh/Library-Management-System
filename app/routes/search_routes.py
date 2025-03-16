from flask import Blueprint, render_template, request, flash
from ..models import Book
from wtforms import Form, StringField, validators

# Create a Blueprint for search routes
search_routes = Blueprint('search_routes', __name__)

# Define Search-Form
class SearchBook(Form):
    title = StringField('Title', [validators.Length(min=2, max=255)])
    author = StringField('Author(s)', [validators.Length(min=2, max=255)])

# Search for books
@search_routes.route('/search_book', methods=['GET', 'POST'])
def search_book():
    form = SearchBook(request.form)
    if request.method == 'POST' and form.validate():
        title = f"%{form.title.data}%"
        author = f"%{form.author.data}%"
        books = Book.query.filter(Book.title.like(title) | Book.author.like(author)).all()
        if not books:
            flash('No results found', 'warning')
        else:
            flash('Results found', 'success')
        return render_template('search_book.html', form=form, books=books)
    return render_template('search_book.html', form=form)