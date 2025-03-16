import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app, db
from app.models import Book, Member, Transaction
from datetime import datetime,date

@pytest.fixture
def client():
    app = create_app()  # Ensure your app has a 'testing' config with in-memory DB
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # creates an db in memory

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Library' in response.data  # Change text based on your template

# ------------ Book Routes ------------

def test_add_book(client):
    response = client.post('/add_book', data={
        'title': 'Test Book',
        'author': 'Author Name',
        'average_rating': 4.5,
        'isbn': '1234567890',
        'isbn13': '1234567890123',
        'language_code': 'EN',
        'num_pages': 150,
        'ratings_count': 20,
        'text_reviews_count': 5,
        'publication_date': '2024-01-01',
        'publisher': 'Test Publisher',
        'total_quantity': 5
    }, follow_redirects=True)
    assert b'Book added successfully!' in response.data
    assert response.status_code == 200

def test_list_books(client):
    response = client.get('/books')
    assert response.status_code == 200

def test_delete_book(client):
    # Add book first
    book = Book(
        title='Temp Book', author='Author', average_rating=4.0, isbn='1234567890',
        isbn13='1234567890123', language_code='EN', num_pages=100,
        ratings_count=10, text_reviews_count=2, publication_date=date(2024, 1, 1),
        publisher='Pub', total_quantity=3, available_quantity=3, rented_count=0
    )
    db.session.add(book)
    db.session.commit()
    
    response = client.post(f'/delete_book/{book.id}', follow_redirects=True)
    assert b'Book deleted successfully!' in response.data

# ------------ Member Routes ------------

def test_add_member(client):
    response = client.post('/add_member', data={
        'name': 'Test Member',
        'email': 'test@example.com'
    }, follow_redirects=True)
    assert b'Member added successfully!' in response.data

def test_list_members(client):
    response = client.get('/members')
    assert response.status_code == 200

def test_delete_member(client):
    member = Member(name='Temp Member', email='temp@example.com', outstanding_debt=0, amount_spent=0)
    db.session.add(member)
    db.session.commit()

    response = client.post(f'/delete_member/{member.id}', follow_redirects=True)
    assert b'Member deleted successfully!' in response.data

# ------------ Search Route ------------

def test_search_book(client):
    response = client.post('/search_book', data={
        'title': 'SomeTitle',
        'author': 'SomeAuthor'
    }, follow_redirects=True)
    assert response.status_code == 200

# ------------ Transaction Routes ------------

def test_issue_book(client):
    # Add Book and Member first
    book = Book(
    title='Temp Book', author='Author', average_rating=4.0, isbn='1234567890',
    isbn13='1234567890123', language_code='EN', num_pages=100,
    ratings_count=10, text_reviews_count=2,
    publication_date=datetime.strptime('2024-01-01', '%Y-%m-%d').date(),
    publisher='Pub', total_quantity=3, available_quantity=3, rented_count=0
    )
    member = Member(name='Member1', email='mem@example.com', outstanding_debt=0, amount_spent=0)
    db.session.add(book)
    db.session.add(member)
    db.session.commit()

    response = client.post('/issue_book', data={
        'book_id': book.id,
        'member_id': member.id,
        'per_day_fee': 10.0
    }, follow_redirects=True)
    assert b'Book issued successfully!' in response.data

def test_list_transactions(client):
    response = client.get('/transactions')
    assert response.status_code == 200

# ------------ Reports ------------

def test_reports(client):
    response = client.get('/reports')
    assert response.status_code == 200
