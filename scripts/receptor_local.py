"""Receptor local temporario (127.0.0.1:8765): grava em data/investing/<nome>.json o que o navegador enviar por POST /save?name=<nome>. So aceita nomes simples. Parar com Ctrl+C / matar o processo."""
import http.server, json, re, urllib.parse, pathlib
OUT = pathlib.Path("data/investing"); OUT.mkdir(parents=True, exist_ok=True)
class H(http.server.BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.0"
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*"); self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type"); self.send_header("Access-Control-Allow-Private-Network", "true")
    def do_OPTIONS(self): self.send_response(204); self._cors(); self.end_headers()
    def do_POST(self):
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query); nome = (q.get("name", ["x"])[0])
        if not re.fullmatch(r"[A-Za-z0-9_\-]{1,40}", nome): self.send_response(400); self._cors(); self.end_headers(); return
        corpo = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        (OUT / f"{nome}.json").write_bytes(corpo); self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(b"ok")
    def log_message(self, *a): pass
http.server.ThreadingHTTPServer(("127.0.0.1", 8765), H).serve_forever()
