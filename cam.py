import cv2
import requests
import tkinter as tk
from threading import Thread

# Define username and password for the camera
username = "administrator"
password = "12345678"
ip = "192.168.1.156"

# RTSP URL
rtsp_url = f"rtsp://{username}:{password}@{ip}:88/videoMain"

# PTZ URL template
ptz_url_template = "http://{ip}:88/cgi-bin/CGIProxy.fcgi?cmd={cmd}&usr={usr}&pwd={pwd}"

# Function to send PTZ command
def send_ptz_command(cmd):
    url = ptz_url_template.format(ip=ip, cmd=cmd, usr=username, pwd=password)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Check the result in the response XML
            if "<result>0</result>" in response.text:
                print(f"PTZ Command '{cmd}' successful.")
            else:
                print(f"PTZ Command '{cmd}' failed.")
        else:
            print(f"Failed to send PTZ command: {response.status_code}")
    except Exception as e:
        print(f"Error sending PTZ command: {e}")

# Function to display video stream
def display_stream():
    # Capture the video stream
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Error: Unable to connect to camera.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to fetch frame.")
            break
        cv2.imshow("IP Camera Stream", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Function to move PTZ up
def move_up(event=None):
    send_ptz_command('ptzMoveUp')

# Function to move PTZ down
def move_down(event=None):
    send_ptz_command('ptzMoveDown')

# Function to move PTZ left
def move_left(event=None):
    send_ptz_command('ptzMoveLeft')

# Function to move PTZ right
def move_right(event=None):
    send_ptz_command('ptzMoveRight')

# Function to stop PTZ movement (sent on button release)
def stop_ptz_move(event=None):
    send_ptz_command('ptzStopRun')

# Create the main window
window = tk.Tk()
window.title("IP Camera PTZ Control")

# Create buttons for PTZ control with button release binding
btn_up = tk.Button(window, text="Up", width=10, height=2)
btn_up.grid(row=0, column=1)
btn_up.bind("<ButtonPress-1>", lambda e: move_up())  # On press, move up
btn_up.bind("<ButtonRelease-1>", stop_ptz_move)  # On release, stop movement

btn_down = tk.Button(window, text="Down", width=10, height=2)
btn_down.grid(row=2, column=1)
btn_down.bind("<ButtonPress-1>", lambda e: move_down())  # On press, move down
btn_down.bind("<ButtonRelease-1>", stop_ptz_move)  # On release, stop movement

btn_left = tk.Button(window, text="Left", width=10, height=2)
btn_left.grid(row=1, column=0)
btn_left.bind("<ButtonPress-1>", lambda e: move_left())  # On press, move left
btn_left.bind("<ButtonRelease-1>", stop_ptz_move)  # On release, stop movement

btn_right = tk.Button(window, text="Right", width=10, height=2)
btn_right.grid(row=1, column=2)
btn_right.bind("<ButtonPress-1>", lambda e: move_right())  # On press, move right
btn_right.bind("<ButtonRelease-1>", stop_ptz_move)  # On release, stop movement

btn_center = tk.Button(window, text="Center", width=10, height=2, command=lambda: send_ptz_command('ptzReset'))
btn_center.grid(row=1, column=1)

# Start video stream in a separate thread
stream_thread = Thread(target=display_stream, daemon=True)
stream_thread.start()

# Start the Tkinter event loop
window.mainloop()

