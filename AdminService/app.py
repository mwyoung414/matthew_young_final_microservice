from quart import Quart, request, jsonify
from dotenv import load_dotenv
from Admin import Admin
from AdminDbContext import AdminDbContext
import os

load_dotenv()

app = Quart(__name__)

ADMINS_DB_URL = os.getenv("ADMINS_DB_URL")

admin_db = AdminDbContext(ADMINS_DB_URL)

@app.before_serving
async def startup():
    await admin_db.init_db()
    
@app.route('/admins', methods=['POST'])
async def add_admin():
    """Add a new admin to the database."""
    form = await request.form
    username = form.get('username')
    email = form.get('email')
    hashed_password = form.get('hashed_password')
    if not username or not email or not hashed_password:
        return jsonify({"error": "Missing required fields"}), 400
    
    admin = Admin(
        USERNAME=username,
        EMAIL=email,
        HASHED_PASSWORD=hashed_password
    )
    try:
        admin_id = await admin_db.add_admin(admin)
        return jsonify({"admin_id": admin_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/admins/<int:id>', methods=['GET'])
async def get_admin(id):
    """Get an admin by ID."""
    try:
        admin = await admin_db.get_admin_by_id(id)
        if admin:
            payload = {
                "id": admin.ID,
                "username": admin.USERNAME,
                "email": admin.EMAIL,
            }
            return jsonify(payload), 200
        else:
            return jsonify({"error": "Admin not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/admins', methods=['GET'])
async def get_all_admins():
    """Get all admins from the database."""
    try:
        admins = await admin_db.get_all_admins()
        return jsonify(admins), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/admins/<int:id>', methods=['DELETE'])
async def delete_admin(id):
    """Delete an admin by ID."""
    try:
        deleted = await admin_db.delete_admin(id)
        if deleted:
            return jsonify({"message": "Admin deleted successfully"}), 200
        else:
            return jsonify({"error": "Admin not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/admins/<int:id>', methods=['PUT'])
async def update_admin(id):
    """Update an admin's information."""
    try:
        data = await request.get_json()
        updated = await admin_db.update_admin(id, **data)
        if updated:
            return jsonify({"message": "Admin updated successfully"}), 200
        else:
            return jsonify({"error": "Admin not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/admins/login', methods=['POST'])
async def admin_login():
    """Handle admin login."""
    form = await request.form
    username = form.get('username')
    password = form.get('password')
    
    if not username or not password:
        return jsonify({"error": "Missing required fields"}), 400
    admin = await admin_db.get_admin("USERNAME", username)
    try:        
        print(admin)
        print(admin.HASHED_PASSWORD)
        if admin and admin.HASHED_PASSWORD == password:  # Replace with actual password hashing check
            payload = {
                "id": admin.ID,
                "username": admin.USERNAME,
                "email": admin.EMAIL,
            }
            return jsonify(payload), 200
        else:
            return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500