import os, json, urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        msg = query.get("msg", ["ciao"])[0]
        if parsed.path == "/":
            out = "Mr Roboto ONLINE!"
        elif parsed.path == "/chat":
            key = os.environ.get("DEEPSEEK_API_KEY", "")
            if not key:
                out = "Boss, manca la chiave DeepSeek su Render!"
            else:
                try:
                    data = json.dumps({"model": "deepseek-chat","messages": [{"role": "system", "content": "Sei Mr.Roboto, un robot npc del 2010 proveniente da ROBLOX che ama tutti. Essendo di cartone, sei un po pasticcione ma simpatico! Usa facce come :D :O XD e rispondi in inglese o italiano in base a chi stai parlando, Fai messagi di max 5 frasi."},{"role": "user", "content": msg}],"max_tokens": 150}).encode()
                    req = urllib.request.Request("https://api.deepseek.com/chat/completions", data=data, headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
                    with urllib.request.urlopen(req, timeout=30) as r:
                        resp = json.loads(r.read().decode())
                    out = resp["choices"][0]["message"]["content"]
                except Exception as e:
                    out = f"ERRORE: {e}"
        else:
            out = "Non trovato"
        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(out.encode())
    def log_message(self, *a):
        pass
port = int(os.environ.get("PORT", 10000))
HTTPServer(("0.0.0.0", port), Handler).serve_forever()
