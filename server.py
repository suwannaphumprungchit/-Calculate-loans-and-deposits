# -*- coding: utf-8 -*-
"""
server.py  -  ตัวเชื่อมระหว่างหน้าเว็บ (index.html, style.css) กับไฟล์ Python (Deposit.py, loan.py)

วิธีใช้:  python server.py
แล้วเบราว์เซอร์จะเปิดหน้า http://localhost:8000 ให้เอง (ปิดโปรแกรมด้วย Ctrl+C)
ใช้เฉพาะ Python ที่ติดตั้งมาอยู่แล้ว ไม่ต้องติดตั้งอะไรเพิ่ม
"""
import json
import os
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer

import Deposit   # ส่วนคำนวณเงินฝาก
import loan      # ส่วนคำนวณเงินกู้

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = 8000
FILES = {"/": "index.html", "/index.html": "index.html", "/style.css": "style.css"}
TYPES = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8"}


# แต่ละที่อยู่ (URL) ของ API เรียกฟังก์ชันของไฟล์ Python ที่เกี่ยวข้อง
def api_deposit(d):
    return Deposit.calculate(d.get("principal"), d.get("years"), d.get("add"), d.get("rate"), d.get("months"))


def api_loan(d):
    return loan.calculate(d.get("amount"), d.get("years"), d.get("rate"), d.get("months"))


def api_loan_balance(d):
    return loan.balance_after(d.get("amount"), d.get("years"), d.get("rate"), d.get("months"), d.get("k"))


ROUTES = {"/api/deposit": api_deposit, "/api/loan": api_loan, "/api/loan/balance": api_loan_balance}


class Handler(BaseHTTPRequestHandler):
    def send_bytes(self, code, body, content_type):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def send_json(self, code, data):
        self.send_bytes(code, json.dumps(data, ensure_ascii=False).encode("utf-8"), "application/json; charset=utf-8")

    def do_GET(self):
        name = FILES.get(self.path.split("?")[0])
        if not name:
            self.send_bytes(404, "ไม่พบหน้านี้".encode("utf-8"), "text/plain; charset=utf-8")
            return
        with open(os.path.join(HERE, name), "rb") as f:
            self.send_bytes(200, f.read(), TYPES[os.path.splitext(name)[1]])

    def do_POST(self):
        handler = ROUTES.get(self.path)
        if not handler:
            self.send_json(404, {"error": "ไม่พบบริการนี้"})
            return
        try:
            size = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(size).decode("utf-8") or "{}")
            self.send_json(200, handler(data))
        except ValueError as err:          # ค่าที่กรอกไม่ถูกต้อง (รวมถึง JSON เสีย)
            self.send_json(400, {"error": str(err)})
        except Exception:                  # ข้อผิดพลาดอื่น ๆ
            self.send_json(500, {"error": "เกิดข้อผิดพลาดในการคำนวณ"})

    def log_message(self, fmt, *args):     # ไม่ต้องแสดงบันทึกทุกคำขอ
        pass


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://localhost:{PORT}"
    print(f"เปิดโปรแกรมแล้วที่ {url}  (กด Ctrl+C เพื่อปิด)")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nปิดโปรแกรมแล้ว")