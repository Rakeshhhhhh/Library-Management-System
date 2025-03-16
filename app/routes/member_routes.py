from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models import Member, db
from wtforms import Form, StringField, validators

# Create a Blueprint for member routes
member_routes = Blueprint('member_routes', __name__)

# Define Add-Member-Form
class AddMember(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min=6, max=50)])

# List all members
@member_routes.route('/members')
def list_members():
    members = Member.query.all()
    return render_template('members.html', members=members)

# Add a new member
@member_routes.route('/add_member', methods=['GET', 'POST'])
def add_member():
    form = AddMember(request.form)
    if request.method == 'POST' and form.validate():
        new_member = Member(
            name=form.name.data,
            email=form.email.data,
            outstanding_debt=0,
            amount_spent=0
        )
        db.session.add(new_member)
        db.session.commit()
        flash('Member added successfully!', 'success')
        return redirect(url_for('member_routes.list_members'))
    return render_template('add_member.html', form=form)

# View details of a member
@member_routes.route('/member/<int:id>')
def view_member(id):
    member = Member.query.get_or_404(id)
    return render_template('view_member_details.html', member=member)

# Edit a member
@member_routes.route('/edit_member/<int:id>', methods=['GET', 'POST'])
def edit_member(id):
    member = Member.query.get_or_404(id)
    form = AddMember(request.form, obj=member)
    if request.method == 'POST' and form.validate():
        form.populate_obj(member)
        db.session.commit()
        flash('Member updated successfully!', 'success')
        return redirect(url_for('member_routes.list_members'))
    return render_template('edit_member.html', form=form, member=member)

# Delete a member
@member_routes.route('/delete_member/<int:id>', methods=['POST'])
def delete_member(id):
    member = Member.query.get_or_404(id)
    db.session.delete(member)
    db.session.commit()
    flash('Member deleted successfully!', 'success')
    return redirect(url_for('member_routes.list_members'))