import http.server
import json
import hashlib
import hmac

PORT = 8081
SECRET = "SYSTEM_CORE_BETA_2026".encode()

class MockCommandHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Serve a CHANGE_PERSONALITY command
        command = {
            "command": "CHANGE_PERSONALITY",
            "params": {"personality": "Performance"}
        }
        json_data = json.dumps(command)
        
        # Sign it
        signature = hmac.new(SECRET, json_data.encode(), hashlib.sha256).hexdigest()
        
        print(f"\n[SERVER] Serving Command to {self.client_address}")
        
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('X-Evolution-Signature', signature)
        self.end_headers()
        self.wfile.write(json_data.encode())

if __name__ == "__main__":
    print(f"Starting Mock Command Server on port {PORT}...")
    server = http.server.HTTPServer(('localhost', PORT), MockCommandHandler)
    server.handle_request() # Handle one request and exit
