from quart import Quart, request, jsonify
from dotenv import load_dotenv
from Customer import Customer
from CustomerDbContext import CustomerDbContext
import os
from argon2 import PasswordHasher

load_dotenv()

app = Quart(__name__)
ph = PasswordHasher()


CUSTOMER_DB_URL = os.getenv("CUSTOMER_DB_URL")
customer_db = CustomerDbContext(CUSTOMER_DB_URL)
@app.before_serving
async def startup():
    await customer_db.init_db()
    
@app.route('/customers', methods=['POST'])
async def add_customer():
    """Add a new customer to the database."""
    form = await request.form
    username = form.get('username')
    firstname = form.get('firstname')
    lastname = form.get('lastname')
    email = form.get('email')
    phone = form.get('phone')
    address = form.get('address')
    city = form.get('city')
    state = form.get('state')
    zipcode = form.get('zipcode')
    hashed_password = ph.hash(form.get('password'))
    customer = Customer(
        USERNAME=username,
        FIRSTNAME=firstname,
        LASTNAME=lastname,
        EMAIL=email,
        PHONE=phone,
        ADDRESS=address,
        CITY=city,
        STATE=state,
        ZIPCODE=zipcode,
        HASHED_PASSWORD=hashed_password
    )
    try:
        customer_id = await customer_db.add_customer(customer)
        return jsonify({"customer_id": customer_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/customers/<int:id>', methods=['GET'])
async def get_customer(id):
    """Get a customer by ID."""
    try:
        customer = await customer_db.get_customer_by_id(id)
        if customer:
            payload = {
                "id": customer.ID,
                "firstname": customer.FIRSTNAME,
                "lastname": customer.LASTNAME,
                "email": customer.EMAIL,
                "phone": customer.PHONE,
                "address": customer.ADDRESS,
                "city": customer.CITY,
                "state": customer.STATE,
                "zipcode": customer.ZIPCODE
            }
            return jsonify(payload), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/customers/<int:id>', methods=['DELETE'])
async def delete_customer(id):
    """Delete a customer by ID."""
    try:
        deleted = await customer_db.delete_customer(id)
        if deleted:
            return jsonify({"message": "Customer deleted successfully"}), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/customers/<int:id>', methods=['PUT'])
async def update_customer(id):
    """Update a customer's information."""
    try:
        data = await request.get_json()
        updated = await customer_db.update_customer(id, **data)
        if updated:
            return jsonify({"message": "Customer updated successfully"}), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/customers', methods=['GET'])
async def get_all_customers():
    """Get all customers from the database."""
    try:
        if not (payload := await customer_db.get_all_customers()):
            return jsonify({"message": "No customers found"}), 404
        
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/customers/username/<string:username>', methods=['GET'])
async def get_customer_by_username(username):
    """Get a customer by username."""
    try:
        customer = await customer_db.get_customer_by_username(username)
        if customer:
            payload = {
                "id": customer.ID,
                "username": customer.USERNAME,
                "firstname": customer.FIRSTNAME,
                "lastname": customer.LASTNAME,
                "email": customer.EMAIL,
                "phone": customer.PHONE,
                "address": customer.ADDRESS,
                "city": customer.CITY,
                "state": customer.STATE,
                "zipcode": customer.ZIPCODE
            }
            return jsonify(payload), 200
        else:
            return jsonify({"error": "Customer not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500