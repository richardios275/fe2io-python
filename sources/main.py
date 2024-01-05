# Copyright 2023 Sheila Abigaile (Legal Name: Abraham Richard Sunjaya)
# See the full text of the Apache License 2.0 in the LICENSE file at the root of this project.

import os
import sys
import argparse
from PyQt6 import QtCore, QtGui, QtWidgets
import asyncio
import websockets
import requests
import json
from ui.MainUI_ui import Ui_MainWindow
from audioPlayer import set_audio, set_volume, toggle_death_volume, toggle_leave, toggle_fadein

# Variables
args = None
debounce = False
on_death = 1 # 0 = Nothing, 1 = Quieten, 2 = Stop
on_leave = 1 # 0 = Nothing, 1 = Stop
program_files = 'fe2io_files'
urls = {0: "ws://client.fe2.io:8081", 1: "wss://liquid-breakout-bot.onrender.com/socket/websocket"}
icon_links = {0: "http://cdn.discordapp.com/attachments/1060689121116426302/1060699627529175130/FE2IO_Logo.png", 1: "https://liquidbreakout.com/ioClient/assets/WebBasedAudioPlayerLogo.png"}

# Create program folder if it doesn't exist
if not os.path.exists(program_files):
    os.makedirs(program_files)

# Handle Websocket
async def connect_ws(username, uri_option, status_label):
    uri = urls[uri_option]
    print(uri, uri_option)
    async with websockets.connect(uri) as websocket:
        if uri_option == 0:
            message_to_send = username
            await websocket.send(message_to_send)
            print(f"Sent message: {message_to_send}")

            status_label.setText("Status: Connected as " + username)

            while True:
                response = await websocket.recv()
                print(f"Received response: {response}")

                try:
                    data = json.loads(response)
                    if 'msgType' in data:
                        if data['msgType'] == 'bgm':
                            set_audio(data['audioUrl'])
                        if data['msgType'] == 'gameStatus':
                            if data['statusType'] == 'died':
                                toggle_death_volume(on_death)
                            elif data['statusType'] == 'left':
                                if on_leave == 1:
                                    toggle_leave()
                except json.JSONDecodeError:
                    pass
        elif uri_option == 1:
            data = {"type": "connect", "connectionType": "io", "username": username}
            json_data = json.dumps(data)
            await websocket.send(json_data)
            print(f"Sent message: {json_data}")

            while True:
                response = await websocket.recv()
                print(f"Received response: {response}")

                try:
                    data = json.loads(response)
                    if 'type' in data:
                        if data['type'] == 'connectSuccess':
                            status_label.setText("Status: Connected as " + username)
                    elif 'status' in data:
                        if data['status'] == 'ingame':
                            set_audio(data['bgm'], data['startUtcTime'])
                        if data['status'] == 'died':
                            print('Player dead')
                            toggle_death_volume(on_death)
                except json.JSONDecodeError:
                    pass

# Load the Main UI
class MyMainWindow(QtWidgets.QDialog, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Set Window to fixed
        self.setFixedSize(self.size())

        # Load image at the top
        self.load_pixmap(icon_links[0])

        # Set UI according to arguments
        self.lineEdit.setText(args.username)
        self.volume_label.setText(f"Volume: {args.volume}%")
        self.volume_slider.setValue(args.volume)
        self.server_box.setCurrentIndex(1 if args.server == 'lbio' else 0)
        set_volume(args.volume)

        # Automatically connect if --auto-connect argument is used
        if args.auto_connect == True:
            if len(args.username) > 0:
                self.on_connect_button_clicked()
            else:
                print('Argument -u must be used for auto-connect')

        # Connect the UI's to signals
        self.connect_button.clicked.connect(self.on_connect_button_clicked)
        self.fade_box.stateChanged.connect(self.on_fade_box_state_changed)
        self.volume_slider.valueChanged.connect(self.on_slider_value_changed)

        #Radio Buttons
        self.death_quiten.toggled.connect(self.on_death_radio_button_toggled)
        self.death_stop.toggled.connect(self.on_death_radio_button_toggled)
        self.death_nothing.toggled.connect(self.on_death_radio_button_toggled)

        self.leave_stop.toggled.connect(self.on_death_radio_button_toggled)
        self.leave_nothing.toggled.connect(self.on_death_radio_button_toggled)
        self.server_box.currentIndexChanged.connect(self.on_server_box_index_changed)
        
        # Timer to periodically run the event loop
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.run_asyncio_event_loop)
        self.timer.start(100)  # Run every 100 milliseconds

    def run_asyncio_event_loop(self):
        # Run the asyncio event loop
        asyncio.get_event_loop().run_until_complete(asyncio.sleep(0))

    # UI Functions
    def load_pixmap(self, url):
        # Extract the filename from the URL
        file_name = os.path.join("fe2io_files", os.path.basename(url))

        # Check if the file already exists
        if os.path.exists(file_name):
            # Load the image from the local file
            pixmap = QtGui.QPixmap(file_name)
        else:
            # File doesn't exist, download and save it
            response = requests.get(url)
            if response.status_code == 200:
                with open(file_name, "wb") as f:
                    f.write(response.content)

                # Load the image from the local file
                pixmap = QtGui.QPixmap(file_name)
            else:
                # Handle the case when the download fails
                print(f"Failed to download image from {url}")
                return  # Stop further processing if the download fails

        # Scale the image
        scaled_pixmap = pixmap.scaled(self.iconLabel.size(), QtCore.Qt.AspectRatioMode.KeepAspectRatio)

        # Set the image
        self.iconLabel.setPixmap(scaled_pixmap)


    def on_connect_button_clicked(self):
        global debounce
        if debounce == False:
            debounce = True
            self.connect_button.setEnabled(False)
            self.connect_button.setText("Connected")
            username = self.lineEdit.text()
            self.status_label.setText("Status: Connecting")
            asyncio.ensure_future(connect_ws(username, self.server_box.currentIndex(), self.status_label))

    def on_quiten_box_state_changed(value):
        global death_volume_reduction
        death_volume_reduction = False

    def on_fade_box_state_changed(value):
        toggle_fadein(value)

    def on_slider_value_changed(self, value):
        set_volume(value)
        self.volume_label.setText(f"Volume: {value}%")

    def on_death_radio_button_toggled(self):
        global on_death
        if self.death_nothing.isChecked():
            on_death = 0
        elif self.death_quiten.isChecked():
            on_death = 1
        elif self.death_stop.isChecked():
            on_death = 2

    def on_leave_radio_button_toggled(self):
        global on_leave
        if self.leave_nothing.isChecked():
            on_leave = 0
        elif self.leave_stop.isChecked():
            on_leave = 1

    def on_server_box_index_changed(self):
        if self.server_box.currentIndex() == 0:
            self.load_pixmap(icon_links[0])
        elif self.server_box.currentIndex() == 1:
            self.load_pixmap(icon_links[1])

# Arguments and stuff
def main():
    global args
    parser = argparse.ArgumentParser(description="Use FE2.IO without a web browser!")
    parser.add_argument('-u', '--username', help='Set username on startup.', default='')
    parser.add_argument('-v', '--volume', help='Specify volume on startup. (0 - 100)', default=70, type=int)
    parser.add_argument('-s', '--server', help='Specify which server to connect on startup. (Options: fe2io, lbio) Default: fe2io', default='fe2io')
    parser.add_argument('--auto-connect', help='Automatically connect to server on launch. (Arguments -u)', action='store_true')

    args = parser.parse_args()
    print(args)

    if args.username:
        print(args.username)

if __name__ == "__main__":
    main()
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())



# if __name__ == "__main__":
#     asyncio.get_event_loop().run_until_complete(connect_ws())