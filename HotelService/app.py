from quart import Quart, request, jsonify, render_template
from Hotel import Hotel
from HotelDbContext import HotelDbContext, select, func
import os


HOTELS_DB_URL = os.getenv("HOTELS_DB_URL")

hotels_db = HotelDbContext(HOTELS_DB_URL)

app = Quart(__name__)

@app.before_serving
async def startup():
    await hotels_db.init_db()
    
        # count existing hotels
    async with hotels_db.session() as sess:
        result = await sess.execute(
            select(func.count(Hotel.ID))  # Ensure counting a specific column
        )
        count = result.scalar()  # Use scalar() to fetch the count directly

    if count == 0:
        # no data yet, so seed
        await hotels_db.seed_from_parquet("/app/static/usa_hotels.parquet")
        app.logger.info("Database seeded with initial data.")
    else:
        app.logger.info(f"Skipping seed; {count} rows already in hotels table")
    
@app.route('/hotels', methods=['POST'])
async def add_hotel():
    """Add a new hotel to the database."""
    data = await request.get_json()
    
    data = dict(data)
    hotel = Hotel(
        NAME=data['name'],
        HOTELRATING=data['rating'],
        ADDRESS=data['address'],
        CITY=data['city'],
        STATE=data['state'],
        DESCRIPTION=data['description']
    )
    
    try:
        hotel_id = await hotels_db.add_hotel(hotel)
        return jsonify({"hotel_id": hotel_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/hotels', methods=['GET'])
async def get_hotels():
    """Get all hotels."""
    try:
        hotels = await hotels_db.get_all_hotels()
        payload = [h.to_dict() for h in hotels]
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/hotels/<int:id>', methods=['GET'])
async def get_hotel(id):
    """Get a hotel by ID."""
    try:
        hotel = await hotels_db.get_hotel_by_id(id)
        if hotel:
            payload = {
                "id": hotel.ID,
                "name": hotel.HOTELNAME,
                "address": hotel.ADDRESS,
                "city": hotel.CITY,
                "state": hotel.STATE,
                "rating": hotel.HOTELRATING,
                "description": hotel.DESCRIPTION,
            }
            return jsonify(payload), 200
        else:
            return jsonify({"error": "Hotel not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/hotels/<int:id>', methods=['DELETE'])
async def delete_hotel(id):
    """Delete a hotel by ID."""
    try:
        result = await hotels_db.delete_hotel(id)
        if result:
            return jsonify({"message": "Hotel deleted successfully"}), 200
        else:
            return jsonify({"error": "Hotel not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/hotels', methods=['PUT'])
async def update_hotel(id):
    """Update a hotel's information."""
    try:
        if request.form:
            form = await request.form
            data = {
                "name": form.get('name'),
                "address": form.get('address'),
                "city": form.get('city'),
                "state": form.get('state'),
                "rating": form.get('rating'),
                "description": form.get('description'),
            }
        else:
            data = await request.get_json()
            data = dict(data)
            data = {
                "name": data.get('name'),
                "address": data.get('address'),
                "city": data.get('city'),
                "state": data.get('state'),
                "rating": data.get('rating'),
                "description": data.get('description'),
            }
        updated = await hotels_db.update_hotel(id, **data)
        if updated:
            return jsonify({"message": "Hotel updated successfully"}), 200
        else:
            return jsonify({"error": "Hotel not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500