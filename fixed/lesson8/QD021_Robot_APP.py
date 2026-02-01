# This is a fixed version and that the original can be downloaded from https://acebott.com/product/acebott-qd021-bionic-biped-robot-kit-for-arduino-esp32-electronic-toy-programming/?srsltid=AfmBOoq9a9pHc1a1ynt7Tx79tU8Wh5OVMYjRRdCgY6kQDarNoWvZtNEB
import network
import socket
import select
import time
from machine import Pin, PWM, Timer, ADC
import random
from libs.ACB_Biped_Robot import *
import uasyncio as asyncio
import libs.ACB_Biped_Robot

val = 0

ssid = "Biped_Robot"     # Set WIFI name
password = "12345678"    # Set WIFI password
http_port = 80           # Setting the HTTP server port

http_server = None
clients = []

Trig_PIN = 13
Echo_PIN = 14


#          ---------------
#         |     O   O     |
#         |---------------|
# YR 18==> |             | <== YL 5   180-0   180-0
#          ---------------
#             ||     ||
#             ||     ||
# RR 17==> ------   ------ <== RL 16  180-0  180-0
#          |-----   -----|


def setup():
    global http_server
    servo_init(4, 27, 25, 26) # Andr: Corrected pin order (RT=25, RC=26)
    Servo_PROGRAM_Zero() # 90 90 90 90
    Ultrasonic_Init(Trig_PIN,Echo_PIN)
    
    wifi = network.WLAN(network.AP_IF)
    wifi.active(True)
    wifi.config(essid=ssid, password=password, max_clients=5,authmode=network.AUTH_WPA2_PSK)
    print("Ready! Use 'http://{}' to connect".format(wifi.ifconfig()[0]))
    time.sleep(0.1)
    
    http_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    http_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    http_server.bind(('0.0.0.0', http_port))
    http_server.listen(1)

def parse_query_string(query):
    global val
    variables = {}
    
    for param in query.split('&'):
        if '=' in param:
            key, value = param.split('=', 1)
            variables[key] = value
            if key in ['val']:
                # Convert and store only once to avoid redundancy
                if key == 'val':
                    val = int(value) 
    return variables


def handle_http_connection(client):

    request = b''
    
    # The client request is read in a loop until all data is received
    while True:
        part = client.recv(1024)
        time.sleep(0.01)
        request += part
        if len(part) < 1024:
            break
    request_str = request.decode('utf-8')
    
    if request_str.startswith('GET'):
        parts = request_str.split(' ', 2)
        
        if len(parts) < 2:
            raise ValueError("The request format is invalid.")

        _, path = parts[:2]

        if '?' in path:
            endpoint, query = path.split('?')
        else:
            endpoint = path
            query = ""

        if endpoint == '/control':
            variables = parse_query_string(query)
            val = variables.get('val')
            val = int(val)
            print(val)
            
            if val == 8:
                response_data = ""
                response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_data)}\r\n\r\n{response_data}"
                client.send(response.encode('utf-8'))
            
setup()

while True:
    try:
        ready = select.select([http_server], [], [], 0.5)
        if ready[0]:
            if http_server in ready[0]:
                client, _ = http_server.accept()
                handle_http_connection(client)
                client.close()
        
        if val == 1:
            forward()
        elif val == 2:
            backward()
        elif val == 3:
            left()
        elif val == 4:
            right()
        if val == 8:
            stop()
        elif val == 10:
            sprint()
        elif val == 11:
            left_kick()
        elif val == 12:
            right_kick()
        elif val == 13:
            left_tilt()
        elif val == 14:
            right_tilt()
        elif val == 15:
            left_stamp()
        elif val == 16:
            dance()
        elif val == 17:
            avoid()
        elif val == 18:
            follow()
        elif val == 19:
            left_ankles()
        elif val == 20:
            right_stamp()
        elif val == 21:
            right_ankles()
        
    
            
    except Exception as e:
        print("Loop error:", e)
        time.sleep(1)  # Prevent fast restart
