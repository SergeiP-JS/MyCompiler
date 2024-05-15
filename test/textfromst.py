from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QTextCursor


class TextEdit(QtWidgets.QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptRichText(True)
        self.textChanged.connect(self.text_has_changed)
        # maximum number of characters is set to 10
        self.max_count = 10

    def text_has_changed(self):
        # block signals, and save original text cursor
        blocked = self.blockSignals(True)
        old_cursor = self.textCursor()

        # create new cursor for setting char format of part of text before the self.max_count'th character
        cursor = QtGui.QTextCursor(self.document())
        # cursor.setPosition(self.max_count, mode=QtGui.QTextCursor.KeepAnchor)
        # cursor.setPosition(self.max_count)
        # cursor.setVerticalMovement(self.max_count)

        cursor.movePosition(QTextCursor.Start)
        # cursor.movePosition(QTextCursor.Down, mode=QtGui.QTextCursor.MoveMode, int=5)
        cursor.movePosition(QTextCursor.Right, mode=QtGui.QTextCursor.MoveMode, int=10)
        format = QtGui.QTextCharFormat()
        format.setForeground(QtGui.QColor('#000000'))
        cursor.mergeCharFormat(format)
        # change of text format doesn't take effect until text cursor of self is set to updated text cursor.
        self.setTextCursor(cursor)

        # if document contains more than self.max_count: reformat everything that comes after the self.max_count'th character.
        if self.document().characterCount() > self.max_count:
            cursor.setPosition(self.max_count)
            cursor.movePosition(QtGui.QTextCursor.End, mode=QtGui.QTextCursor.KeepAnchor)
            format.setForeground(QtGui.QColor('#a0a0a0'))
            cursor.mergeCharFormat(format)
            self.setTextCursor(cursor)

        # reset text cursor to original cursor and unblock signals.
        self.setTextCursor(old_cursor)
        self.blockSignals(blocked)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    w = TextEdit()
    w.show()
    app.exec()