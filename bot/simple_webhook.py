"""Minimal webhook server using http.server so you can test POST /webhook without Flask.

Usage:
  /bin/python3 simple_webhook.py
Then POST a Dialogflow-style JSON to http://localhost:8080/webhook
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

PORT = 8080

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self, code=200):
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    def do_POST(self):
        if self.path != '/webhook':
            self._set_headers(404)
            self.wfile.write(json.dumps({'error': 'not found'}).encode())
            return

        length = int(self.headers.get('content-length', 0))
        raw = self.rfile.read(length) if length else b''
        try:
            req = json.loads(raw.decode('utf-8')) if raw else {}
        except Exception as e:
            self._set_headers(400)
            self.wfile.write(json.dumps({'error': 'invalid json', 'detail': str(e)}).encode())
            return

        query_result = req.get('queryResult', {})
        intent = query_result.get('intent', {}).get('displayName')
        params = query_result.get('parameters', {})

        if intent == 'Order Status':
            order_no = params.get('order_number') or 'unknown'
            fulfillment = f"Order {order_no}: In transit, expected delivery in 2 days." if order_no != 'unknown' else "Can you share your order number, please?"
        elif intent == 'Shipping Info':
            fulfillment = 'Standard shipping takes 3-5 business days. Express is 1-2 days.'
        elif intent == 'Refund Policy':
            fulfillment = 'You can request a refund within 30 days. Would you like the steps?'
        elif intent == 'Greeting':
            fulfillment = 'Hi there! How can I assist you today?'
        else:
            fulfillment = "Sorry, I didn't get that — could you rephrase?"

        self._set_headers(200)
        self.wfile.write(json.dumps({'fulfillmentText': fulfillment}).encode())

if __name__ == '__main__':
    print(f'Starting simple webhook on port {PORT}...')
    server = HTTPServer(('0.0.0.0', PORT), Handler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Stopping server')
        server.server_close()
