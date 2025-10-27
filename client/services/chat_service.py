from PyQt6.QtCore import QObject, pyqtSignal

class ChatSignals(QObject):
    message_received = pyqtSignal(dict)