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

ssid = "Biped_Robot"       # Set WIFI name
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
    
    # Read the client requests in a loop until all the data has been received
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
        
        if endpoint == '/':
            response_data = '''
                <!doctype html>
<html>
      <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width,initial-scale=1">
          <title>Biped Robot</title>
          <style>

            input[type=range] {
                -webkit-appearance: none;
                width: 80%;
                height: 10px;
                background: #ccc;
                cursor: pointer;
                margin: 10px;
            }

            input[type=range]::-webkit-slider-thumb {
                -webkit-appearance: none;
                width: 20px;
                height: 20px;
                background: #ff3034;
                cursor: pointer;
                border-radius: 50%;
            }

              *{
                  padding: 0; margin: 0;
                  font-family:monospace;
              }

              *{  
                  -webkit-touch-callout:none;  
                  -webkit-user-select:none;  
                  -khtml-user-select:none;  
                  -moz-user-select:none;  
                  -ms-user-select:none;  
                  user-select:none;  
              }

          canvas {
          margin: auto;
          display: block;

          }
          .tITULO{
              text-align: center;
              color: rgb(97, 97, 97);
              
          }
          .LINK{
              color: red;
              width: 60px;
              margin: auto;
              display: block;
              font-size: 14px;
          }
          .cont_flex{
              margin: 20px auto 20px;
              width: 70%;
              max-width: 400px;
              display: flex;
              flex-wrap: wrap;
              justify-content: space-around;
          }
          .cont_flex button{
              width: 80px;
              height: 35px;
              border: none;
              background-color: #3D9EFF;
              border-radius: 10px;
              color: white;

          }
          .cont_flex button:active{
              background-color: #0080FF;
          }

          .cont_flex5{
              margin: 20px auto 20px;
              width: 100%;
              max-width: 400px;
              display: flex;
              flex-wrap: wrap;
              justify-content: space-around;
          }
          .cont_flex5 button{
              width: 280px;
              height: 35px;
              border: none;
              background-color: #3D9EFF;
              border-radius: 10px;
              color: white;
          }

          .cont_flex5 button:active{
              background-color: #0080FF;
          }

          .custom-alert {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: lightskyblue;
            padding: 20px;
            border: 1px solid gray;
            border-radius: 5px;
            animation: fadeInOut 2s ease-in-out forwards;
            opacity: 0; 
            visibility: hidden; 
            }

          input{-webkit-user-select:auto;} 
          input[type=range]{-webkit-appearance:none;width:300px;height:25px;background:#cecece;cursor:pointer;margin:0}
          input[type=range]:focus{outline:0}
          input[type=range]::-webkit-slider-runnable-track{width:100%;height:2px;cursor:pointer;background:#EFEFEF;border-radius:0;border:0 solid #EFEFEF}
          input[type=range]::-webkit-slider-thumb{border:1px solid rgba(0,0,30,0);height:22px;width:22px;border-radius:50px;background:#ff3034;cursor:pointer;-webkit-appearance:none;margin-top:-10px}

          </style>
      </head>

      <body>
          <div id="customAlert" class="custom-alert">
            <p id="alertText" style="color: white; font-size: 15px;"></p>
          </div>

          <p style="color: black; display: flex; justify-content: center; align-items: center; font-size: 25px;">Biped Robot</p>   

          <div class="cont_flex">     
              <button type="button" id="Forward" ontouchstart="ForwardSending('1')"  ontouchend="stopSending()">Forward</button>
          </div>

          <div class="cont_flex">     
              <button type="button" id="turn_left" ontouchstart="turnleftSending('3')"  ontouchend="stopSending()" >Turn<br>Left</button>

              <button type="button" id="Backward" ontouchstart="BackwardSending('2')"  ontouchend="stopSending()" >Backward</button>

              <button type="button" id="turn_right" ontouchstart="turnrightSending('4')"  ontouchend="stopSending()" >Turn<br>Right</button>  
          </div>

          <div class="cont_flex">     
              
          </div>

          <p><br></p>

          <p style="color: black; display: flex; justify-content: center; align-items: center; font-size: 25px;">Sports Mode</p>   

          <div class="cont_flex">   
              <button type="button" id="Rub" ontouchstart="fetch(document.location.origin+'/control?var=robot&val=11');"  ontouchend="stopSending()" >Left<br>Kick</button>

              <button type="button" id="Shadows" ontouchstart="fetch(document.location.origin+'/control?var=robot&val=10');" >Sprint</button>

              <button type="button" id="Swing" ontouchstart="fetch(document.location.origin+'/control?var=robot&val=12');"  ontouchend="stopSending()" >Right<br>Kick</button>
          </div>

          <div class="cont_flex">   
              <button type="button" id="left_tilt"  ontouchstart="fetch(document.location.origin+'/control?var=robot&val=13');" >Left<br>Tilt</button>

              <button type="button" id="Dancing"  ontouchstart="fetch(document.location.origin+'/control?var=robot&val=16');">Dance</button>

              <button type="button" id="right_tilt"  ontouchstart="fetch(document.location.origin+'/control?var=robot&val=14');" >Right<br>Tilt</button>
          </div>

          <div class="cont_flex">   
              <button type="button" id="test1"  ontouchstart="fetch(document.location.origin+'/control?var=robot&val=19');" >Left<br>Ankles</button>

              <button type="button" id="Following"  ontouchend="fetch(document.location.origin+'/control?var=robot&val=18');">Follow</button>

              <button type="button" id="test3"  ontouchstart="fetch(document.location.origin+'/control?var=robot&val=21');" >Right<br>Ankles</button>
          </div>

          <div class="cont_flex">   
              <button type="button" id="Rise"  ontouchstart="fetch(document.location.origin+'/control?var=robot&val=15');" ontouchend="stopSending()">Left<br>Stamp</button>

              <button type="button" id="avoid"  ontouchend="fetch(document.location.origin+'/control?var=robot&val=17');">Avoid</button>

              <button type="button" id="test2"  ontouchstart="fetch(document.location.origin+'/control?var=robot&val=20');" >Right<br>Stamp</button>
          </div>

          <div class="cont_flex5">   
              <button type="button" id="Stop"  ontouchend="fetch(document.location.origin+'/control?var=robot&val=8');">Stop</button>
          </div>

  

          <p><br></p>

          

          <script>
              let intervalId;

              function ForwardSending(value) {
                fetch(document.location.origin+'/control?var=robot&val=' + 1);
                intervalId = setInterval(() => {
                  fetch(document.location.origin+'/control?var=robot&val=' + value);
                }, 1200);
              }

              function turnleftSending(value) {
                fetch(document.location.origin+'/control?var=robot&val=' + 3);
                intervalId = setInterval(() => {
                  fetch(document.location.origin+'/control?var=robot&val=' + value);
                }, 1200);
              }

              function BackwardSending(value) {
                fetch(document.location.origin+'/control?var=robot&val=' + 2);
                intervalId = setInterval(() => {
                  fetch(document.location.origin+'/control?var=robot&val=' + value);
                }, 1200);
              }

              function turnrightSending(value) {
                fetch(document.location.origin+'/control?var=robot&val=' + 4);
                intervalId = setInterval(() => {
                  fetch(document.location.origin+'/control?var=robot&val=' + value);
                }, 1200);
              }

              function RubSending(value) { //Kick the leg
                fetch(document.location.origin+'/control?var=robot&val=' + 11);
                intervalId = setInterval(() => {
                  fetch(document.location.origin+'/control?var=robot&val=' + value);
                }, 1400);
              }

              function SwingSending(value) {
                fetch(document.location.origin+'/control?var=robot&val=' + 12);
                intervalId = setInterval(() => {
                  fetch(document.location.origin+'/control?var=robot&val=' + value);
                }, 1400);
              }

              function left_tiltSending(value) {
                fetch(document.location.origin+'/control?var=robot&val=' + 13);
                intervalId = setInterval(() => {
                  fetch(document.location.origin+'/control?var=robot&val=' + value);
                }, 5000);
              }

              function right_tiltSending(value) {
                fetch(document.location.origin+'/control?var=robot&val=' + 14);
                intervalId = setInterval(() => {
                  fetch(document.location.origin+'/control?var=robot&val=' + value);
                }, 5000);
              }

              function RiseSending(value) {
                fetch(document.location.origin+'/control?var=robot&val=' + 15);
                intervalId = setInterval(() => {
                  fetch(document.location.origin+'/control?var=robot&val=' + value);
                }, 2400);
              }

              function stopSending() {
                clearInterval(intervalId);
                fetch(document.location.origin+'/control?var=robot&val=8');
              }

              window.onload = function(){
                  var canvas = document.getElementById("canvas");
                  var ctx = canvas.getContext("2d");

                  ctx.fillStyle = "rgb(255,0,0)";
                  ctx.fillRect(73,25,60,35);
                  ctx.clearRect(78,30,50,25);

                  ctx.fillRect(93,20,20,5);
                  ctx.fillRect(68,35,5,15);
                  ctx.fillRect(133,35,5,15);

                  ctx.beginPath();
                  ctx.arc(92,42,6,0,2*Math.PI,true);
                  ctx.fill();

                  ctx.beginPath();
                  ctx.arc(117,42,6,0,2*Math.PI,true);
                  ctx.fill();

                  ctx.beginPath();
                  ctx.arc(104,100,35,0,Math.PI,true);
                  ctx.fill();

                  ctx.clearRect(50,85,100,20);

              }
          
              document.addEventListener(
              'DOMContentLoaded',function(){
                  function b(B){let C;switch(B.type){case'checkbox':C=B.checked?1:0;break;case'range':case'select-one':C=B.value;break;case'button':case'submit':C='1';break;default:return;}const D=`${c}/control?var=${B.id}&val=${C}`;fetch(D).then(E=>{console.log(`request to ${D} finished, status: ${E.status}`)})}var c=document.location.origin;const e=B=>{B.classList.add('hidden')},f=B=>{B.classList.remove('hidden')},g=B=>{B.classList.add('disabled'),B.disabled=!0},h=B=>{B.classList.remove('disabled'),B.disabled=!1},i=(B,C,D)=>{D=!(null!=D)||D;let E;'checkbox'===B.type?(E=B.checked,C=!!C,B.checked=C):(E=B.value,B.value=C),D&&E!==C?b(B):!D&&('aec'===B.id?C?e(v):f(v):'agc'===B.id?C?(f(t),e(s)):(e(t),f(s)):'awb_gain'===B.id?C?f(x):e(x):'face_recognize'===B.id&&(C?h(n):g(n)))};document.querySelectorAll('.close').forEach(B=>{B.onclick=()=>{e(B.parentNode)}}),fetch(`${c}/status`).then(function(B){return B.json()}).then(function(B){document.querySelectorAll('.default-action').forEach(C=>{i(C,B[C.id],!1)})});const j=document.getElementById('stream'),k=document.getElementById('stream-container'),l=document.getElementById('get-still'),m=document.getElementById('toggle-stream'),n=document.getElementById('face_enroll'),o=document.getElementById('close-stream'),p=()=>{window.stop(),m.innerHTML='Start Stream'},q=()=>{j.src=`${c+':81'}/stream`,f(k),m.innerHTML='Stop Stream'};l.onclick=()=>{p(),j.src=`${c}/capture?_cb=${Date.now()}`,f(k)},o.onclick=()=>{p(),e(k)},m.onclick=()=>{const B='Stop Stream'===m.innerHTML;B?p():q()},n.onclick=()=>{b(n)},document.querySelectorAll('.default-action').forEach(B=>{B.onchange=()=>b(B)});const r=document.getElementById('agc'),s=document.getElementById('agc_gain-group'),t=document.getElementById('gainceiling-group');r.onchange=()=>{b(r),r.checked?(f(t),e(s)):(e(t),f(s))};const u=document.getElementById('aec'),v=document.getElementById('aec_value-group');u.onchange=()=>{b(u),u.checked?e(v):f(v)};const w=document.getElementById('awb_gain'),x=document.getElementById('wb_mode-group');w.onchange=()=>{b(w),w.checked?f(x):e(x)};const y=document.getElementById('face_detect'),z=document.getElementById('face_recognize'),A=document.getElementById('framesize');A.onchange=()=>{b(A),5<A.value&&(i(y,!1),i(z,!1))},y.onchange=()=>{return 5<A.value?(alert('Please select CIF or lower resolution before enabling this feature!'),void i(y,!1)):void(b(y),!y.checked&&(g(n),i(z,!1)))},z.onchange=()=>{return 5<A.value?(alert('Please select CIF or lower resolution before enabling this feature!'),void i(z,!1)):void(b(z),z.checked?(h(n),i(y,!0)):g(n))}});
          
          </script>
      </body>
</html>
            '''
            response = f"HTTP/1.1 200 OK\r\nContent-Length: {len(response_data)}\r\n\r\n{response_data}"
            client.send(response.encode('utf-8'))
            
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
            val = 8
        elif val == 2:
            backward()
            val = 8
        elif val == 3:
            left()
            val = 8
        elif val == 4:
            right()
            val = 8
        if val == 8:
            stop()
        elif val == 10:
            sprint()
            val = 8
        elif val == 11:
            left_kick()
            val = 8
        elif val == 12:
            right_kick()
            val = 8
        elif val == 13:
            left_tilt()
            val = 8
        elif val == 14:
            right_tilt()
            val = 8
        elif val == 15:
            left_stamp()
            val = 8
        elif val == 16:
            dance()
            val = 8
        elif val == 17:
            avoid()
        elif val == 18:
            follow()
        elif val == 19:
            left_ankles()
            val = 8
        elif val == 20:
            right_stamp()
            val = 8
        elif val == 21:
            right_ankles()
            val = 8
        
    
            
    except Exception as e:
        print("Loop error:", e)
        time.sleep(1)  # Prevent rapid restarts
