from flask import Blueprint, render_template
from ..models import Member, Book

# Create a Blueprint for report routes
report_routes = Blueprint('report_routes', __name__)

# Generate reports
@report_routes.route('/reports')
def reports():
    top_members = Member.query.order_by(Member.amount_spent.desc()).limit(5).all()
    top_books = Book.query.order_by(Book.rented_count.desc()).limit(5).all()
    return render_template('reports.html', members=top_members, books=top_books)