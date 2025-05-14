from quart import Quart, jsonify, request
from Booking import Booking
from BookingDbContext import BookingDbContext
from dotenv import load_dotenv
import os
import http

load_dotenv()

app = Quart(__name__)


BOOKINGS_DB_URL = os.getenv("BOOKINGS_DB_URL")

bookings_db = BookingDbContext(BOOKINGS_DB_URL)

@app.before_serving
async def startup():
    await bookings_db.init_db()
    

@app.route('/bookings', methods=['GET'])
async def get_bookings():
    """Get all bookings from the database."""
    try:
        bookings = await bookings_db.get_all_bookings()
        payload = [b.to_dict() for b in bookings]
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/bookings', methods=['POST'])
async def add_booking():
    """Add a new booking to the database."""
    data = await request.get_json()
    
    data = dict(data)
    booking = Booking(
        HOTELID=data['hotel_id'],
        CUSTOMERID=data['customer_id'],
        ROOM_TYPE=data['room_type'],
        NUM_OF_ROOMS=data['num_of_rooms'],      
        CHECKINDATE=data['checkin_date'],
        CHECKOUTDATE=data['checkout_date'],
        NUMBER_OF_NIGHTS=data['number_of_nights'],
        TOTAL_PRICE=data['total_price']
    )
    
    try:    
        booking_id = await bookings_db.add_booking(booking)
        return jsonify({"booking_id": booking_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/bookings/<int:user_id>', methods=['GET'])
async def get_bookings_by_user(user_id):
    """Get all bookings for a specific user."""
    try:
        bookings = await bookings_db.get_bookings_by_user_id(user_id)
        payload = [b.to_dict() for b in bookings]
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
