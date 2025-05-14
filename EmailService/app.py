from quart import Quart, request, jsonify
from EmailService import Email
import os
app = Quart(__name__)

app_password = os.getenv("APP_PASSWORD")

email_service = Email.EmailService("mwyoung43@gmail.com", app_password)

@app.route('/send_email', methods=['POST'])
async def send_email():
    """Send an email."""
    data = await request.get_json()
    to_addr = data.get("to")
    subject = data.get("subject")
    body = data.get("body")

    if not all([to_addr, subject, body]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        email_service.send_email(to_addr, subject, body)
        return jsonify({"message": "Email sent successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
