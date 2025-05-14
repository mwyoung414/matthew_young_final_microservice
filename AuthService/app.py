from quart import Quart, render_template, request, redirect, url_for, jsonify
from JWT import JWTService
from functools import wraps

app = Quart(__name__)

# Initialize JWTService with a secret key
jwt_service = JWTService(secret_key="your_secret_key")

# Middleware to protect routes
def token_required(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"error": "Token is missing or invalid"}), 401

        token = auth_header.split(' ')[1]
        payload = jwt_service.verify_token(token)
        if not payload:
            return jsonify({"error": "Token is invalid or expired"}), 401

        # Pass the payload to the route
        return await f(payload, *args, **kwargs)

    return decorated_function

@app.route('/customer_login', methods=['GET', 'POST'])
async def customer_login():
    if request.method == 'POST':
        form = await request.form
        username = form.get('username')
        password = form.get('password')
        # Perform authentication (replace with actual logic)
        if username == "customer" and password == "password":
            return jwt_service.create_token(user_id=1, username=username, role="customer")  # Return tokens as JSON
        return {"error": "Invalid credentials"}, 401
    return await render_template('index.html')

@app.route('/admin_login', methods=['GET', 'POST'])
async def admin_login():
    if request.method == 'POST':
        form = await request.form
        username = form.get('username')
        password = form.get('password')
        # Perform authentication (replace with actual logic)
        if username == "admin" and password == "adminpass":
            return jwt_service.create_token(user_id=1, username=username, role="admin")  # Return tokens as JSON
        return {"error": "Invalid credentials"}, 401
    return await render_template('index.html')

@app.route('/protected', methods=['GET'])
@token_required
async def protected_route(payload):
    return {"message": "This is a protected route", "user": payload}

@app.route('/admin', methods=['GET'])
@token_required
async def admin_dashboard(payload):
    return {"message": "Welcome to the admin dashboard", "user": payload}

