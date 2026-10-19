import http.server
import socketserver
import json
import os
import recovery_engine
import shutil

PORT = 8001

class RecoveryHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/scan':
            print("Received scan request from UI!")
            output_dir = "./Recovered_Photos"
            
            # Clean up previous runs
            if os.path.exists(output_dir):
                shutil.rmtree(output_dir)
            
            try:
                # Actually run the python engine on the fake drive!
                recovery_engine.recover_jpegs("fake_drive.img", output_dir)
                
                files = []
                if os.path.exists(output_dir):
                    files = os.listdir(output_dir)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                response = {"status": "success", "files_found": len(files), "files": files}
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                print("Error:", e)
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == "__main__":
    Handler = RecoveryHandler
    print(f"Backend Server running at port {PORT}")
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
