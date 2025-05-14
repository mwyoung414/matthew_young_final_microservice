from quart import Quart, render_template, jsonify, request
from dotenv import load_dotenv
from functools import wraps
import httpx

app = Quart(__name__)

load_dotenv()
@app.after_request
def add_headers(response):
    """Modify response headers to enable CORS.

    This function adds headers to the HTTP response to allow
    Cross-Origin Resource Sharing (CORS) from any origin.

    Args:
        response: The Flask response object.

    Returns:
        The modified Flask response object.
    """
    response.headers['Access-Control-Allow-Origin'] = "*"
    response.headers['Access-Control-Allow-Headers'] = "Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With"
    response.headers['Access-Control-Allow-Methods'] = "GET, POST, PUT, DELETE OPTIONS"
    return response


@app.route('/', methods=['GET'])
async def index():
    
    hotel_url = "http://localhost:30084/hotels"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(hotel_url)
            hotels = response.json() if response.status_code == 200 else []
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {hotel_url}: {exc}")
        hotels = []
    return await render_template('index.html', hotels=hotels)

@app.route('/register', methods=['GET'])
async def register():
    state_url = "http://localhost:30081/states"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(state_url)
            states = response.json() if response.status_code == 200 else []
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {state_url}: {exc}")
        states = []  # Fallback to an empty list if the request fails
    return await render_template('register.html', states=states)

@app.route('/customers', methods=['POST'])
async def add_customer():
    """Add a new customer to the database."""
    customer_url = "http://localhost:30082/customers"
    try:
        data = await request.get_json()
        async with httpx.AsyncClient() as client:
            response = await client.post(customer_url, json=data)
            if response.status_code == 201:
                return jsonify({"customer_id": response.json().get("customer_id")}), 201
            else:
                return jsonify({"error": "Failed to add customer"}), response.status_code
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {customer_url}: {exc}")
        return jsonify({"error": "Request failed"}), 500
    
@app.route('/admin/login', methods=['POST'])
async def admin_login():
    """Handle admin login."""
    form = await request.form
    data = dict(form)

    if 'password' in data:
        data['hashed_password'] = data['password']
    get_admin_url = "http://localhost:30083/admins/login"
    try:     
        async with httpx.AsyncClient() as client:
            response = await client.post(get_admin_url, data=data)
            if response.status_code == 200:
                return await render_template('base_admin.html')
            else:
                return jsonify({"error": "Invalid credentials"}), response.status_code
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {get_admin_url}: {exc}")
        return jsonify({"error": "Request failed"}), 500
    
@app.route('/view_users', methods=['GET'])
async def view_users():
    """View all users."""
    get_all_users_url = "http://localhost:30082/customers"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(get_all_users_url)
            if response.status_code != 200:
                return jsonify({"error": "Failed to retrieve users"}), response.status_code
            users = response.json()
            return await render_template('view_users.html', users=users)
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {get_all_users_url}: {exc}")
        return jsonify({"error": "Request failed"}), 500
    
@app.route('/book/hotel/<int:hotel_id>', methods=['GET'])
async def book_hotel(hotel_id):
    
    get_hotel_url = f"http://localhost:30084/hotels/{hotel_id}"
    get_rooms_url = "http://localhost:30081/rooms"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(get_hotel_url)
            if response.status_code != 200:
                return jsonify({"error": "Failed to retrieve hotel"}), response.status_code
            hotel = response.json()
            response = await client.get(get_rooms_url)
            if response.status_code != 200:
                return jsonify({"error": "Failed to retrieve rooms"}), response.status_code
            rooms = response.json()
            return await render_template('book_hotel.html', hotel=hotel, rooms=rooms)
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {get_hotel_url}: {exc}")
    return await render_template('book_hotel.html', hotel_id=hotel_id)

@app.route('/checkout', methods=['GET'])
async def checkout():
    """Handle checkout process."""
    booking = dict(request.args)
    print(f"checkout: {booking}")
    return await render_template('checkout.html', booking=booking)
    
    
@app.route('/customer_dashboard', methods=['POST'])
async def customer_dashboard():
    """Render the customer dashboard."""

    form = await request.form
    data = dict(form)
    username = data.get("username")
    password = data.get("password")
    
    customer_url = f"http://localhost:30082/customers/username/{username}"   
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(customer_url)
            if response.status_code == 200:
                customer = response.json()
            else:
                return jsonify({"error": "Failed to retrieve customer data"}), response.status_code
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {customer_url}: {exc}")
        return jsonify({"error": "Request failed"}), 500
    return await render_template('customer_dashboard.html', customer=customer)

@app.route('/view_hotels', methods=['GET'])
async def view_hotels():
    """View all hotels."""
    hotel_url = "http://localhost:30084/hotels"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(hotel_url)
            if response.status_code != 200:
                return jsonify({"error": "Failed to retrieve hotels"}), response.status_code
            hotels = response.json()
            return await render_template('view_hotels.html', hotels=hotels)
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {hotel_url}: {exc}")
        return jsonify({"error": "Request failed"}), 500

@app.route('/confirmation', methods=['POST'])
async def confirmation():
    """Sends the booking information to payment service which sends to booking and transaction service."""
    form = await request.form
    data = dict(form)
    
    payload = {
        "customer_id": 1,
        "hotel_id": data.get("hotel_id"),
        "room_type": data.get("room_type"),
        "num_of_rooms": data.get("num_of_rooms"),
        "total_price": data.get("total_price"),
        "check_in_date": data.get("checkin_date"),
        "check_out_date": data.get("checkout_date"),
        "number_of_nights": data.get("number_of_nights"),
        
    }
    
    print(f"confirmation: {payload}")
    
    Payment_URL = "http://localhost:30088/process_payment"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(Payment_URL, json=payload)
            if response.status_code != 201:
                try:
                    return response.json(), response.status_code
                except Exception:
                    return {"error": response.text}, response.status_code
    except httpx.RequestError as exc:
        print(f"An error occurred while requesting {Payment_URL}: {exc}")
        return jsonify({"error": "Request failed"}), 500
    return await render_template('confirmation.html', booking=payload)

