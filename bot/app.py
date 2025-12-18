"""Flask webhook to handle Dialogflow fulfillment requests.

This provides simple canned responses and demonstrates how to read intent & parameters.
"""
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/webhook", methods=["POST"])
def webhook():
    req = request.get_json(force=True)
    # Dialogflow v2 format: queryResult.intent.displayName, parameters
    query_result = req.get("queryResult", {})
    intent = query_result.get("intent", {}).get("displayName")
    params = query_result.get("parameters", {})

    if intent == "Order Status":
        order_no = params.get("order_number") or "unknown"
        # In production, look up DB or external service here
        fulfillment = f"Order {order_no}: In transit, expected delivery in 2 days." if order_no != "unknown" else "Can you share your order number, please?"
    elif intent == "Shipping Info":
        fulfillment = "Standard shipping takes 3-5 business days. Express is 1-2 days."
    elif intent == "Refund Policy":
        fulfillment = "You can request a refund within 30 days. Would you like the steps?"
    elif intent == "Greeting":
        fulfillment = "Hi there! How can I assist you today?"
    else:
        fulfillment = "Sorry, I didn't get that — could you rephrase?"

    return jsonify({"fulfillmentText": fulfillment})


if __name__ == "__main__":
    app.run(port=8080, debug=True)
