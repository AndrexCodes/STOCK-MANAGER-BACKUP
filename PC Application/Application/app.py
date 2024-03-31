from flask import Flask, request, jsonify
from flask_cors import CORS
from printer import receipt_print, correct_print
import json
import threading

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5 import QtGui

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stock Manage Software")
        self.setWindowIcon(QtGui.QIcon('simba_app.png'))
        self.setGeometry(100, 100, 800, 600)

        self.browser = QWebEngineView()
        self.setCentralWidget(self.browser)
        # url = QUrl("http://127.0.0.1:5500/webapp/index.html")
        # self.browser.load(url)

        with open("config.json", "r+") as json_file:
            data = json_file.read()
            data = json.loads(data)
            url = data["html_file"]

            # Load remote web pages
            url = QUrl.fromLocalFile(url)
            self.browser.load(url)

app = Flask(__name__)
CORS(app)

def run_pyqt5():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

def run_flask():
    app.run(debug=False, host='127.0.0.1', port=5555)

@app.route("/printing", methods=["GET", "POST"])
def PrintReceipt():
    request_data = request.get_json()
    print(request_data)
    if request_data:
        data = request_data["print_details"]
        data = correct_print(data)
        state = receipt_print(data)
        return jsonify({
            "state": state,
            "message": "Recipt Print Succesful"
        })
    return jsonify({
            "state": False,
            "message": "Unknown Error occures"
        })

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    pyqt5_thread = threading.Thread(target=run_pyqt5)
    pyqt5_thread.start()

    # Joining threads
    flask_thread.join()
    pyqt5_thread.join()
    