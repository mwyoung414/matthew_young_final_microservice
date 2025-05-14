from quart import Quart, jsonify, request
import httpx


app = Quart(__name__)

BOOKING_SERVICE_URL = "http://localhost:30085/bookings"
TRANSACTION_SERVICE_URL = "http://localhost:30087/transactions"

@app.route('/process_payment', methods=['GET'])
async def test():
    """Test endpoint to check if the service is running."""
    return jsonify({"message": "Payment service is running"}), 200

@app.route('/process_payment', methods=['POST'])
async def process_payment():
    """Process a payment."""
    print(request)
    data = await request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    price = data.get("price")
    if price is None:
        price = data.get("total_price")

    def to_int(val):
        try:
            return int(val)
        except (TypeError, ValueError):
            return val
    def to_float(val):
        try:
            return float(val)
        except (TypeError, ValueError):
            return val

    booking_data = {
        "customer_id": to_int(data.get("customer_id")),
        "hotel_id": to_int(data.get("hotel_id")),
        "room_type": data.get("room_type"),
        "price": to_float(price),
        "num_of_rooms": to_int(data.get("num_of_rooms")),
        "check_in_date": data.get("check_in_date"),
        "check_out_date": data.get("check_out_date"),
        "number_of_nights": to_int(data.get("number_of_nights")),
        "total_price": to_float(data.get("total_price")),
    }
    
    transaction_data = {
        "customer_id": to_int(data.get("customer_id")),
        "hotel_id": to_int(data.get("hotel_id")),
        "price": to_float(price),
        "room_type": data.get("room_type"),
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response_book = await client.post(BOOKING_SERVICE_URL, json=booking_data)
            print(f"Booking service status: {response_book.status_code}, response: {response_book.text}")
            response_transaction = await client.post(TRANSACTION_SERVICE_URL, json=transaction_data)
            print(f"Transaction service status: {response_transaction.status_code}, response: {response_transaction.text}")

            if response_book.status_code == 201 and response_transaction.status_code == 201:
                return jsonify({"message": "Payment processed successfully"}), 200
            elif response_book.status_code != 201:
                return jsonify({
                    "error": "Failed to book hotel",
                    "details": response_book.text
                }), response_book.status_code
            else:
                return jsonify({
                    "error": "Failed to record transaction",
                    "details": response_transaction.text
                }), response_transaction.status_code
    except httpx.RequestError as exc:
        print(f"An error occurred while processing payment: {exc}")
        return jsonify({"error": "Request failed", "details": str(exc)}), 500