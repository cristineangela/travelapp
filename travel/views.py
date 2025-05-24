from flask import Blueprint, render_template, request, redirect, url_for, flash 
from .models import Destination, Booking
from flask_login import current_user, login_required
from . import db

mainbp = Blueprint('main', __name__)

@mainbp.route('/')
def index():
    destinations = db.session.scalars(db.select(Destination)).all()    
    return render_template('index.html', destinations=destinations)

@mainbp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        statement = db.select(Destination).where(Destination.description.like(query))
        destinations = db.session.scalars(statement).all()
        return render_template('index.html', destinations=destinations)
    else:
        return redirect(url_for('main.index'))
    
@mainbp.route('/book/<int:destination_id>')
@login_required
def book_destination(destination_id):
    destination = Destination.query.get_or_404(destination_id)

    new_booking = Booking(user_id=current_user.id, destination_id=destination.id)
    db.session.add(new_booking)
    db.session.commit()

    flash(f"Successfully booked: {destination.name}")
    return redirect(url_for('main.bookings'))

@mainbp.route('/bookings')
@login_required
def bookings():
    user_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('bookings.html', bookings=user_bookings)