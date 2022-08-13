import sys
import datetime
from PyQt6 import uic, QtCore, QtGui, QtWidgets
import requests
from requests.exceptions import HTTPError
import json


class MainWindow(QtWidgets.QMainWindow):
    ServerAdress = "http://localhost:5000"
    MessageId = 0

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        uic.loadUi('messanger.ui', self)
        self.pushButton1.clicked.connect(self.pushButton1_clicked)

    def pushButton1_clicked(self):
        self.SendMessage()

    def SendMessage(self):
        UserName = self.lineEdit1.text()
        MessageText = self.lineEdit2.text()
        TimeStamp = str(datetime.datetime.today())
        msg = f"{{\"UserName\": \"{UserName}\", \"MessageText\": \"{MessageText}\", \"TimeStamp\": \"{TimeStamp}\"}}"
        # {"UserName": Irina, "MessageText": "Privet", "TimeStamp":20-02-20}

        print("Отправлено сообщение:" + msg)
        url = self.ServerAdress + "/api/Messanger"
        print(str(url))
        data = json.loads(msg)
        r = requests.post(url, json=data)

    def GetMessage(self, id):
        url = self.ServerAdress + "/api/Messanger/" + str(id)
        # print(url)
        try:
            response = requests.get(url)
            # если ответ успешен, исключения задействованы не будут
            response.raise_for_status()
        except HTTPError as http_err:
            print(f"HTTP error occured: {http_err}")
            return None
        except Exception as err:
            print(f"Other error occured: {err}")
            return None
        else:
            text = response.text
            #print(text)
            return text

    def timerEvent(self):
        msg = self.GetMessage(self.MessageId)
        if msg is not None:
            msg = json.loads(msg)
            #print(msg)
            UserName = msg["UserName"]
            MessageText = msg["MessageText"]
            TimeStamp = msg["TimeStamp"]
            msgtext = f"{TimeStamp} : <{UserName}> : {MessageText}"
            #print(msgtext)
            self.listWidget1.insertItem(self.MessageId, msgtext)
            self.MessageId += 1
            msg = self.GetMessage(self.MessageId)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    timer = QtCore.QTimer()
    time = QtCore.QTime(0, 0, 0)
    timer.timeout.connect(w.timerEvent)
    timer.start(3000)
    sys.exit(app.exec())
