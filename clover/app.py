from flask import Flask, jsonify, request
from collections import deque
import threading

app = Flask(__name__)

# 數據存儲
tickets = {}
next_ticket_id = 1
service_windows = {
    1: {"id": 1, "name": "服務窗口A", "serving_ticket_id": None},
    2: {"id": 2, "name": "服務窗口B", "serving_ticket_id": None},
}
waiting_queue = deque()

# 鎖
lock = threading.Lock()

@app.route('/api/service_windows', methods=['GET'])
def get_service_windows():
    return jsonify(list(service_windows.values()))

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    global next_ticket_id
    with lock:
        new_ticket_id = next_ticket_id
        tickets[new_ticket_id] = {"id": new_ticket_id, "status": "waiting"}
        next_ticket_id += 1
        waiting_queue.append(new_ticket_id)
        return jsonify(tickets[new_ticket_id]), 201

@app.route('/api/service_windows/<int:window_id>/tickets', methods=['POST'])
def assign_ticket_to_window(window_id):
    if window_id not in service_windows:
        return jsonify({"error": "Service window not found"}), 404
    with lock:
        if not waiting_queue:
            return jsonify({"error": "No tickets in waiting queue"}), 400
        ticket_id = waiting_queue.popleft()
        service_windows[window_id]["serving_ticket_id"] = ticket_id
        tickets[ticket_id]["status"] = f"serving at {service_windows[window_id]['name']}"
        return jsonify(tickets[ticket_id])

@app.route('/api/service_windows/<int:window_id>/next', methods=['POST'])
def next_customer(window_id):
    if window_id not in service_windows:
        return jsonify({"error": "Service window not found"}), 404
    with lock:
        if not waiting_queue:
             # 如果沒有等待的，就將當前服務的設為 None
            service_windows[window_id]["serving_ticket_id"] = None
            return jsonify(service_windows[window_id])
        ticket_id = waiting_queue.popleft()
        service_windows[window_id]["serving_ticket_id"] = ticket_id
        tickets[ticket_id]["status"] = f"serving at {service_windows[window_id]['name']}"
        return jsonify(service_windows[window_id])

if __name__ == '__main__':
    app.run(debug=True, port=5001)
