import sys
from PyQt6 import QtCore, QtGui, QtWidgets
import asyncio
import websockets
import json
from window import Ui_MainWindow
from audioPlayer import download_and_play_audio

# Variables
debounce = False
volume = 70
death_volume_reduction = True

# Global UI
global_ui = []

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
                        asyncio.ensure_future(download_and_play_audio(data['audioUrl']))
                    if data['msgType'] == 'gameStatus' and data['Status'] == 'died':
                        print('Player dead')
            except json.JSONDecodeError:
                pass  # Ignore non-JSON messages

# Load the Main UI
class MyMainWindow(QtWidgets.QDialog, Ui_MainWindow):
    


    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # Append UIs to the Global UI thing
        global global_ui
        global_ui.append(self.status_label)

        # Connect the button's clicked signal to the custom function
        self.connect_button.clicked.connect(self.on_connect_button_clicked)

        # Timer to periodically run the event loop
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.run_asyncio_event_loop)
        self.timer.start(100)  # Run every 100 milliseconds

    def run_asyncio_event_loop(self):
        # Run the asyncio event loop
        asyncio.get_event_loop().run_until_complete(asyncio.sleep(0))

    def on_connect_button_clicked(self):
        global debounce
        if debounce == False:
            debounce = True
            username = self.lineEdit.text()
            print("Connecting")
            self.status_label.setText("Status: Connecting")
            asyncio.ensure_future(connect_ws(username, self.status_label))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())


# if __name__ == "__main__":
#     asyncio.get_event_loop().run_until_complete(connect_ws())