import sys
import traceback

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.Qsci import *
from PyQt5.uic.properties import QtGui

def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions


class CustomMainWindow(QMainWindow):
    def __init__(self):
        super(CustomMainWindow, self).__init__()

        # Window setup
        # --------------

        # 1. Define the geometry of the main window
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle("QScintilla Test")

        # 2. Create frame and layout
        self.__frm = QFrame(self)
        self.__frm.setStyleSheet("QWidget { background-color: #ffeaeaea }")
        self.__lyt = QVBoxLayout()
        self.__frm.setLayout(self.__lyt)
        self.setCentralWidget(self.__frm)
        self.__myFont = QFont()
        self.__myFont.setPointSize(14)

        # 3. Place a button
        self.__btn = QPushButton("Qsci")
        self.__btn.setFixedWidth(50)
        self.__btn.setFixedHeight(50)
        self.__btn.clicked.connect(self.__btn_action)
        self.__btn.setFont(self.__myFont)
        self.__lyt.addWidget(self.__btn)

        # QScintilla editor setup
        # ------------------------

        # ! Make instance of QsciScintilla class!
        self.setStyle
        self.__editor = QsciScintilla()
        self.__editor.setText("Hello\n")
        self.__editor.append("worldыыыы")
        cursor =  self.__editor.cursor()
        # cursor.setPosition(self.max_count, mode=QtGui.QTextCursor.KeepAnchor)
        cursor.setPos(1,1)
        self.__editor.append("Hi")
        self.__editor.setCursor(cursor)

        self.__editor.setMarginsBackgroundColor(QColor("gainsboro"))
        self.__editor.setMarginLineNumbers(1, True)
        self.__editor.setStyleSheet("")


        self.__editor.setLexer(None)
        self.__editor.setUtf8(True)  # Set encoding to UTF-8
        self.__editor.setFont(self.__myFont)  # Will be overridden by lexer!

        # ! Add editor to layout !
        self.__lyt.addWidget(self.__editor)

        self.last_line, self.last_index = None, None

        self.show()

    ''''''

    def __btn_action(self):
        print("Hello World!")
        print(self.__editor.text())
        # format = QtGui.QTextCharFormat()
        # format.setBackground(QtGui.QBrush(QtGui.QColor("red")))

        line, index = self.__editor.getCursorPosition()

        print(self.__editor.getCursorPosition())
        # self.__editor.SendScintilla(QsciScintilla.StraightBoxIndicator, True, 3)

        # indicatorDefine(QsciScintilla.FullBoxIndicator, 5)
        self.__editor.setIndicatorForegroundColor(QColor(255, 0, 255, 128), 5)
        if self.last_line != None:
            self.__editor.clearIndicatorRange(self.last_line, self.last_index, 3, 3, 3)
        self.__editor.fillIndicatorRange(line, index, 3, 3, 3)
        self.last_line, self.last_index = line, index
        # self.__editor.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, index, 10)
        print(self.__editor.getCursorPosition())
        # self.__editor.setCursor(cursor)

        if index < self.__editor.lineLength(line):
            self.__editor.setCursorPosition(line, index + 1)
        elif line < self.__editor.lines():
            self.__editor.setCursorPosition(line + 1, 0)
        print(self.__editor.getCursorPosition())

    ''''''


''' End Class '''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setStyle(QStyleFactory.create('Fusion'))
    myGUI = CustomMainWindow()

    sys.exit(app.exec_())