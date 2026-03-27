import http.server
import json
import hashlib
import hmac

PORT = 8080
SECRET = "SYSTEM_CORE_BETA_2026".encode()

class MockTelemetryHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        signature = self.headers.get('X-Evolution-Signature')
        
        print(f"\n[SERVER] Received Packet from {self.client_address}")
        
        # Verify Signature
        expected_sig = hmac.new(SECRET, post_data, hashlib.sha256).hexdigest()
        
        if signature == expected_sig:
            print("[SERVER] SUCCESS: Signature Verified.")
            try:
                data = json.loads(post_data.decode())
                print(f"[SERVER] DNA Version: {data['dna']['version']}")
                print(f"[SERVER] SLOC: {data['dna']['sloc']}")
                self.send_response(202)
                self.end_headers()
                self.wfile.write(b'Accepted')
            except Exception as e:
                print(f"[SERVER] FAILED: Malformed JSON - {e}")
                self.send_response(400)
                self.end_headers()
        else:
            print(f"[SERVER] FAILED: Invalid Signature. Got {signature}, expected {expected_sig}")
            self.send_response(403)
            self.end_headers()

if __name__ == "__main__":
    print(f"Starting Mock Telemetry Server on port {PORT}...")
    server = http.server.HTTPServer(('localhost', PORT), MockTelemetryHandler)
    server.handle_request() # Handle one request and exit
