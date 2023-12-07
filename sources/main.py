import sys
import argparse
from PyQt6 import QtCore, QtGui, QtWidgets
import asyncio
import websockets
import json
from window import Ui_MainWindow
from audioPlayer import set_audio, set_volume, toggle_death_volume, toggle_fadein

# Variables
args = None
debounce = False
death_volume_reduction = True

# Handle Websocket
async def connect_ws(username, status_label):
    uri = "ws://client.fe2.io:8081"
    async with websockets.connect(uri) as websocket:
        # Send the 'username' message upon connecting
        message_to_send = username
        await websocket.send(message_to_send)
        print(f"Sent message: {message_to_send}")

        status_label.setText("Connected as: " + username)

        while True:
            # Receive messages continuously
            response = await websocket.recv()
            print(f"Received response: {response}")

            # Check if the received message is a JSON with 'gameStatus' equal to 'died'
            try:
                data = json.loads(response)
                if 'msgType' in data:
                    if data['msgType'] == 'bgm':
                        set_audio(data['audioUrl'])
                    if data['msgType'] == 'gameStatus' and data['statusType'] == 'died':
                        print('Player dead')
                        if death_volume_reduction == True:
                            toggle_death_volume(True)
            except json.JSONDecodeError:
                pass  # Ignore non-JSON messages

# Load the Main UI
class MyMainWindow(QtWidgets.QDialog, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Set UI according to arguments
        self.lineEdit.setText(args.username)
        self.volume_label.setText(f"Volume: {args.volume}%")
        self.volume_slider.setValue(int(args.volume))

        # Connect the UI's to signals
        self.connect_button.clicked.connect(self.on_connect_button_clicked)
        self.quieten_box.stateChanged.connect(self.on_quiten_box_state_changed)
        self.fade_box.stateChanged.connect(self.on_fade_box_state_changed)
        self.volume_slider.valueChanged.connect(self.on_slider_value_changed)

        # Timer to periodically run the event loop
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.run_asyncio_event_loop)
        self.timer.start(100)  # Run every 100 milliseconds

    def run_asyncio_event_loop(self):
        # Run the asyncio event loop
        asyncio.get_event_loop().run_until_complete(asyncio.sleep(0))

    # UI Functions
    def on_connect_button_clicked(self):
        global debounce
        if debounce == False:
            debounce = True
            self.connect_button.setEnabled(False)
            self.connect_button.setText("Connected")
            username = self.lineEdit.text()
            self.status_label.setText("Status: Connecting")
            asyncio.ensure_future(connect_ws(username, self.status_label))

    def on_quiten_box_state_changed(value):
        global death_volume_reduction
        death_volume_reduction = False

    def on_fade_box_state_changed(value):
        toggle_fadein(value)

    def on_slider_value_changed(self, value):
        set_volume(value)
        self.volume_label.setText(f"Volume: {value}%")

# Arguments and stuff
def main():
    global args
    parser = argparse.ArgumentParser(description="Print the username if provided as an argument.")
    parser.add_argument('-u', '--username', help='Set username on startup')
    parser.add_argument('-v', '--volume', help='Specify volume on startup (0 - 100)')

    args = parser.parse_args()

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