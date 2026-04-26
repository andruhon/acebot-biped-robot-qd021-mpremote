# Tell the robot to join your WiFi (optional).
#
# Two ways to reach the robot from your computer:
#
#   1. Default. The robot makes its own WiFi called "Biped_Robot"
#      (password "12345678"). Your computer joins that network to
#      talk to the robot. While joined, your computer cannot reach
#      the internet -- unless you have a second WiFi adapter.
#
#   2. With this file. The robot joins the WiFi you already use.
#      Your computer stays on the same network. Both keep internet.
#      No extra adapter needed.
#
# To enable option 2: save this file as wifi_config.py, fill in
# the WiFi name and password below, then upload it:
#
#     mpremote connect /dev/ttyUSB0 fs cp for-agents/wifi_config.py :wifi_config.py
#
# Option 1 still works as a backup.

WIFI_NAME = "MyNetwork"
WIFI_PASSWORD = "your-password-here"
