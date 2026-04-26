# Agent-friendly HTTP server for the Acebott QD021 biped.
#
# Endpoints (all GET, all return 200 with a small JSON or plain-text body):
#
#   /                       human-readable summary of the API
#   /status                 JSON heartbeat: uptime, last command, last distance
#   /distance               ultrasonic reading in centimetres (plain text;
#                           "-1.0" on read failure)
#
#   Movement (each call BLOCKS until the cycles finish, then responds):
#     /forward[?steps=N]    walk forward N cycles  (default 1; max 10)
#     /backward[?steps=N]   walk backward
#     /turn_left[?steps=N]  rotate left in place
#     /turn_right[?steps=N] rotate right in place
#     /stop                 freeze servos (no steps)
#
#     Approximate calibration on a flat smooth surface:
#       - 1 forward / backward cycle ~ 1.5 cm of travel
#       - 8 turn_left / turn_right cycles ~ 90 degrees of rotation
#
#   Trick moves (single cycle each, no steps parameter):
#     /sprint, /dance, /avoid, /follow,
#     /kick_left,  /kick_right,
#     /tilt_left,  /tilt_right,
#     /stamp_left, /stamp_right,
#     /ankles_left, /ankles_right
#
# This is NOT compatible with the lesson7 /control?var=robot&val=N protocol.
# Endpoints are named after the action they perform so an LLM driver can't
# confuse a magic number for a different command.

import network
import socket
import time
import json
from libs.ACB_Biped_Robot import *
import libs.ACB_Biped_Robot

MAX_STEPS = 10

ssid = "Biped_Robot"
password = "12345678"
http_port = 80

http_server = None

Trig_PIN = 13
Echo_PIN = 14

boot_ticks = time.ticks_ms()
last_command = None
last_steps = None
last_command_at_ms = None
last_distance_cm = None


def uptime_ms():
    return time.ticks_diff(time.ticks_ms(), boot_ticks)


def start_sta():
    """Optional: connect to a WiFi network as a station if wifi_config.py
    exists. Returns the assigned IP on success, None otherwise. The AP is
    brought up unconditionally before this — STA is purely additive."""
    try:
        import wifi_config
    except ImportError:
        return None
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(wifi_config.WIFI_NAME, wifi_config.WIFI_PASSWORD)
    for _ in range(20):
        if sta.isconnected():
            return sta.ifconfig()[0]
        time.sleep(0.5)
    print("STA: failed to connect to {}".format(wifi_config.WIFI_NAME))
    sta.active(False)
    return None


def setup():
    global http_server
    servo_init(4, 27, 25, 26)
    Servo_PROGRAM_Zero()
    Ultrasonic_Init(Trig_PIN, Echo_PIN)

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password, max_clients=5, authmode=network.AUTH_WPA2_PSK)
    print("AP: http://{}/".format(ap.ifconfig()[0]))

    sta_ip = start_sta()
    if sta_ip:
        print("STA: http://{}/".format(sta_ip))

    time.sleep(0.1)

    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    http_server.bind(('0.0.0.0', http_port))
    http_server.listen(1)


def parse_query_string(query):
    variables = {}
    for param in query.split('&'):
        if '=' in param:
            key, value = param.split('=', 1)
            variables[key] = value
    return variables


def parse_steps(query):
    if not query:
        return 1
    raw = parse_query_string(query).get('steps')
    if raw is None:
        return 1
    try:
        n = int(raw)
    except Exception:
        return 1
    if n < 1:
        return 1
    if n > MAX_STEPS:
        return MAX_STEPS
    return n


def send_response(client, body='', status='200 OK', content_type='text/plain'):
    body_bytes = body.encode('utf-8') if isinstance(body, str) else body
    headers = (
        "HTTP/1.1 {}\r\n"
        "Content-Type: {}\r\n"
        "Content-Length: {}\r\n"
        "Connection: close\r\n"
        "\r\n"
    ).format(status, content_type, len(body_bytes))
    client.send(headers.encode('utf-8') + body_bytes)


def record_command(name, steps=1):
    global last_command, last_steps, last_command_at_ms
    last_command = name
    last_steps = steps
    last_command_at_ms = uptime_ms()


def run_movement(client, name, motion_fn, query):
    n = parse_steps(query)
    record_command(name, n)
    print("{} x{}".format(name, n))
    for _ in range(n):
        motion_fn()
    send_response(
        client,
        json.dumps({'action': name, 'steps': n}),
        content_type='application/json',
    )


def run_trick(client, name, motion_fn):
    record_command(name, 1)
    print(name)
    motion_fn()
    send_response(
        client,
        json.dumps({'action': name}),
        content_type='application/json',
    )


ROOT_BODY = (
    "Acebott biped robot - agent API.\n\n"
    "Movement (?steps=N optional, max {max}):\n"
    "  GET /forward, /backward, /turn_left, /turn_right\n"
    "  GET /stop\n\n"
    "Sensing:\n"
    "  GET /distance     ultrasonic reading in cm (plain text)\n"
    "  GET /status       JSON heartbeat\n\n"
    "Trick moves (single cycle):\n"
    "  GET /sprint, /dance, /avoid, /follow\n"
    "  GET /kick_left, /kick_right, /tilt_left, /tilt_right\n"
    "  GET /stamp_left, /stamp_right, /ankles_left, /ankles_right\n"
).format(max=MAX_STEPS)


MOVEMENTS = {
    '/forward':    forward,
    '/backward':   backward,
    '/turn_left':  left,
    '/turn_right': right,
}

TRICKS = {
    '/sprint':       sprint,
    '/dance':        dance,
    '/avoid':        avoid,
    '/follow':       follow,
    '/kick_left':    left_kick,
    '/kick_right':   right_kick,
    '/tilt_left':    left_tilt,
    '/tilt_right':   right_tilt,
    '/stamp_left':   left_stamp,
    '/stamp_right':  right_stamp,
    '/ankles_left':  left_ankles,
    '/ankles_right': right_ankles,
}


def handle_http_connection(client):
    global last_distance_cm

    request = b''
    while True:
        part = client.recv(1024)
        time.sleep(0.01)
        request += part
        if len(part) < 1024:
            break
    request_str = request.decode('utf-8')

    if not request_str.startswith('GET'):
        send_response(client, 'method not allowed', status='405 Method Not Allowed')
        return

    parts = request_str.split(' ', 2)
    if len(parts) < 2:
        send_response(client, 'bad request', status='400 Bad Request')
        return
    path = parts[1]

    if '?' in path:
        endpoint, query = path.split('?', 1)
    else:
        endpoint = path
        query = ''

    if endpoint == '/':
        send_response(client, ROOT_BODY)
        return

    if endpoint == '/status':
        send_response(client, json.dumps({
            'uptimeMs': uptime_ms(),
            'lastCommand': last_command,
            'lastSteps': last_steps,
            'lastCommandAtMs': last_command_at_ms,
            'lastDistanceCm': last_distance_cm,
        }), content_type='application/json')
        return

    if endpoint == '/distance':
        try:
            d = libs.ACB_Biped_Robot.Ultrasonic.get_distance()
            last_distance_cm = d
            send_response(client, '{:.1f}'.format(d))
        except Exception as e:
            print('Distance read error:', e)
            send_response(client, '-1.0')
        return

    if endpoint == '/stop':
        record_command('stop', 0)
        stop()
        send_response(client, json.dumps({'action': 'stop'}), content_type='application/json')
        return

    if endpoint in MOVEMENTS:
        run_movement(client, endpoint.lstrip('/'), MOVEMENTS[endpoint], query)
        return

    if endpoint in TRICKS:
        run_trick(client, endpoint.lstrip('/'), TRICKS[endpoint])
        return

    send_response(client, 'unknown endpoint', status='404 Not Found')


setup()

while True:
    try:
        client, _ = http_server.accept()
        handle_http_connection(client)
        client.close()
    except Exception as e:
        print('Loop error:', e)
        time.sleep(1)
