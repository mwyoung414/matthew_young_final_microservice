from quart import Quart, request, jsonify
from StatesDBContext import StatesDbContext
from RoomsDBContext import RoomsDbContext
from dotenv import load_dotenv
import os

load_dotenv()

app = Quart(__name__)

STATE_DB_URL = "mysql+asyncmy://root:password@states-db.default.svc.cluster.local:3306/states"
ROOMS_DB_URL = "mysql+asyncmy://root:password@rooms-db.default.svc.cluster.local:3306/rooms"


states_db = StatesDbContext(STATE_DB_URL)
rooms_db = RoomsDbContext(ROOMS_DB_URL)


@app.before_serving
async def create_db():
    await states_db.init_db()
    await rooms_db.init_db()

@app.route('/states', methods=['GET'])
async def get_states():
    """Get all states from the database."""
    try:
        # Assuming you have a function to fetch states from the database
        states = await states_db.get_all_states()
        payload = [
            {
                "code": state.code,
                "name": state.name,
            }
            for state in states
        ]
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/rooms', methods=['GET'])
async def get_rooms():
    """Get all rooms from the database."""
    try:
        # Assuming you have a function to fetch rooms from the database
        rooms = await rooms_db.get_all_rooms()
        payload = [
            {
                "id": room.id,
                "room_type": room.room_type,
                "price": str(room.price),
            }
            for room in rooms
        ]
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/rooms/<room_type>', methods=['GET'])
async def get_room_price(room_type):
    """Get the price of a room by type."""
    try:
        # Assuming you have a function to fetch room price from the database
        room = await rooms_db.get_price_by_type(room_type)
        if room:
            payload = {
                "id": room.id,
                "room_type": room.room_type,
                "price": str(room.price),
            }
            return jsonify(payload), 200
        else:
            return jsonify({"error": "Room not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
