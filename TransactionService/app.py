from quart import Quart, request, jsonify

from Transaction import Transaction
from TransactionsDbContext import TransactionsDbContext

app = Quart(__name__)

TRANSACTIONS_DB_URL = "mysql+asyncmy://root:password@transactions-db.default.svc.cluster.local:3306/transactions"

transaction_db = TransactionsDbContext(TRANSACTIONS_DB_URL)

@app.before_serving
async def startup():
    """Initialize the database before serving."""
    await transaction_db.init_db()

@app.route('/transactions', methods=['GET'])
async def get_transactions():
    """Get all transactions from the database."""
    try:
        transactions = await transaction_db.get_all_transactions()
        payload = [t.to_dict() for t in transactions]
        return jsonify(payload), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/transctions', methods=['POST'])
async def add_transaction():
    """Add a new transaction to the database."""
    data = await request.get_json()
    transaction = Transaction(
        id=data['id'],
        customer_id=data['customer_id'],
        hotel_id=data['hotel_id'],
        price=data['price'],
        room_type=data['room_type'],
    )
    
    try:
        transaction_id = await transaction_db.add_transaction(transaction)
        return jsonify({"transaction_id": transaction_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
