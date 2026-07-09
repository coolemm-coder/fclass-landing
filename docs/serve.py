#!/usr/bin/env python3
"""FC Dashboard — локальный прокси-сервер. Запуск: python3 serve.py"""
import http.server, urllib.request, ssl, socket, json, os

PORT = 8765
N8N_IP = '91.218.143.156'
N8N_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJjYmU3ZWU3My1mMmY3LTRmMDMtYmM2ZC1jN2Y0MDcyMDcyMTciLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzY5MTY0OTY3fQ.mcot7vYqR2c_H8dHKLhIeNVEwUg5KHbIlRWSVgr1NdU'

orig_gai = socket.getaddrinfo
socket.getaddrinfo = lambda h,*a,**kw: orig_gai(N8N_IP if h=='automation.landingpro.by' else h,*a,**kw)
ctx = ssl.create_default_context(); ctx.check_hostname=False; ctx.verify_mode=ssl.CERT_NONE

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.path.dirname(os.path.abspath(__file__)), **kwargs)

    def do_GET(self):
        if self.path == '/fc-stats':
            try:
                req = urllib.request.Request('https://automation.landingpro.by/webhook/fc-stats')
                data = urllib.request.urlopen(req, context=ctx, timeout=10).read()
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self.send_response(502)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
        else:
            super().do_GET()

    def log_message(self, fmt, *args): pass

if __name__ == '__main__':
    with http.server.HTTPServer(('', PORT), Handler) as httpd:
        print(f'✅ FC Dashboard: http://localhost:{PORT}/email-dashboard.html')
        httpd.serve_forever()
