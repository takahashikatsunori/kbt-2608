#!/usr/bin/env python3
"""
kbt-2608 Local HTTP & REST Helper Server
Provides:
1. Static hosting for map tiles and preview pages.
2. REST endpoint GET /api/pdf that redirects or serves dynamic PDF downloads.
"""

import http.server
import socketserver
import urllib.parse
import os
import sys

PORT = int(os.environ.get('PORT', 8000))

class MapRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Enable CORS for all local requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        
        # REST Endpoint: GET /api/pdf
        if parsed.path == '/api/pdf':
            query = urllib.parse.parse_qs(parsed.query)
            lat = query.get('lat', ['35.726'])[0]
            lng = query.get('lng', ['139.475'])[0]
            zoom = query.get('zoom', ['16'])[0]
            bearing = query.get('bearing', ['0'])[0]
            pitch = query.get('pitch', ['0'])[0]
            qr = query.get('qr', ['0'])[0]

            # Redirect to pdf-download.html with parameters
            target_url = f"/pdf-download.html?lat={lat}&lng={lng}&zoom={zoom}&bearing={bearing}&pitch={pitch}"
            if qr in ['1', 'true']:
                target_url += "&qr=1"
            elif qr in ['2', 'large']:
                target_url += "&qr=2"
            self.send_response(302)
            self.send_header('Location', target_url)
            self.end_headers()
            return

        super().do_GET()

def run(port=PORT):
    with socketserver.TCPServer(("", port), MapRequestHandler) as httpd:
        print(f"Map server running at http://localhost:{port}/")
        print(f"  - Preview: http://localhost:{port}/pdf-preview.html")
        print(f"  - REST API: http://localhost:{port}/api/pdf?lat=35.726&lng=139.475&zoom=16")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else PORT
    run(port)
