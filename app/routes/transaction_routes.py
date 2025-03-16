from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Transaction, Book, Member, db
from datetime import datetime
from wtforms import Form, SelectField, FloatField, validators

# Create a Blueprint for transaction routes
transaction_routes = Blueprint('transaction_routes', __name__)

# Define Issue-Book-Form
class IssueBook(Form):
    book_id = SelectField('Book ID', coerce=int)
    member_id = SelectField('Member ID', coerce=int)
    per_day_fee = FloatField('Per Day Renting Fee', [validators.NumberRange(min=1)])

class ReturnBook(Form):
    amount_paid = FloatField('Amount Paid', [validators.NumberRange(min=0)])

# List all transactions
@transaction_routes.route('/transactions')
def list_transactions():
    transactions = Transaction.query.all()
    return render_template('transactions.html', transactions=transactions)

# Issue a book
@transaction_routes.route('/issue_book', methods=['GET', 'POST'])
def issue_book():
    form = IssueBook(request.form)
    form.book_id.choices = [(book.id, book.title) for book in Book.query.all()]
    form.member_id.choices = [(member.id, member.name) for member in Member.query.all()]
    if request.method == 'POST' and form.validate():
        book = Book.query.get(form.book_id.data)
        if book.available_quantity < 1:
            flash('No copies of this book are available to be rented', 'danger')
            return render_template('issue_book.html', form=form)
        new_transaction = Transaction(
            book_id=form.book_id.data,
            member_id=form.member_id.data,
            per_day_fee=form.per_day_fee.data
        )
        book.available_quantity -= 1
        book.rented_count += 1
        db.session.add(new_transaction)
        db.session.commit()
        flash('Book issued successfully!', 'success')
        return redirect(url_for('transaction_routes.list_transactions'))
    return render_template('issue_book.html', form=form)

# Return a book
@transaction_routes.route('/return_book/<int:transaction_id>', methods=['GET', 'POST'])
def return_book(transaction_id):
    transaction = Transaction.query.get_or_404(transaction_id)
    form = ReturnBook(request.form)
    if request.method == 'POST' and form.validate():
        transaction.returned_on = datetime.utcnow()
        transaction.total_charge = (datetime.utcnow() - transaction.borrowed_on).days * transaction.per_day_fee
        transaction.amount_paid = form.amount_paid.data
        member = Member.query.get(transaction.member_id)
        member.outstanding_debt += transaction.total_charge - form.amount_paid.data
        member.amount_spent += form.amount_paid.data
        book = Book.query.get(transaction.book_id)
        book.available_quantity += 1
        db.session.commit()
        flash('Book returned successfully!', 'success')
        return redirect(url_for('transaction_routes.list_transactions'))
    return render_template('return_book.html', form=form, transaction=transaction)