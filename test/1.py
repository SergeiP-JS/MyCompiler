import sys
import builtins

from PyQt5.Qsci import QsciScintilla
from PyQt5.QtGui import QFont
from antlr4 import *
from antlr4.error import ErrorListener
from antlr4.tree.Tree import TerminalNodeImpl




# import MyErrorListener
from Java8Lexer import Java8Lexer
from Java8Parser import Java8Parser
from Java8ParserListener import *

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QPushButton, \
    QProgressDialog, QMessageBox, QStyleFactory, QHBoxLayout, QTabWidget, QLineEdit, QTextEdit
from PyQt5.QtCore import *


class Main(QWidget):
    def __init__(self):

        super().__init__()

        self.setWindowTitle('Code')
        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel('')

        self.tokens = QTreeWidget()
        self.tokens.setHeaderLabel('')

        self.tab = QTabWidget()
        self.tab.addTab(self.tree, "Дерево")
        self.tab.addTab(self.tokens, "Токены")

        self.error = QTreeWidget()
        self.error.setHeaderLabel('Ошибки')
        self.error.setFixedHeight(100)

        self.bp = QPushButton('Получить токены и построить дерево')
        self.bp.clicked.connect(self._on_click)
        self.setStyleSheet('color: blue')
        self.bp.setStyleSheet("background-color: green; color: yellow")
        self.setStyle(QStyleFactory.create(QStyleFactory.keys()[2]))
        # self.setFixedSize(800, 480)
        self.setMinimumSize(800, 480)


        layout = QVBoxLayout()
        layout_H=QHBoxLayout()
        layout_H.addWidget(self.tab)
        # code = QTreeWidget()
        # code.header().hide()

        input_stream = FileStream("C:\Javalib\example.java")
        self.__editor = QsciScintilla()
        self.__editor.setText("Hello\n")
        self.__editor.append("worldыыыы")

        self.__editor.setLexer(None)
        self.__editor.setUtf8(True)  # Set encoding to UTF-8
        self.__myFont = QFont()
        self.__myFont.setPointSize(14)
        self.__editor.setFont(self.__myFont)  # Will be overridden by lexer!
        # layout_H.addWidget(code)
        layout_H.addWidget(self.__editor)

        layout.addLayout(layout_H)
        layout.addWidget(self.error)
        layout.addWidget(self.bp)
        self.setLayout(layout)

    def main(self):
          # argv
        input_stream = FileStream("C:\Javalib\example.java")
        print(input_stream)
        lexer = Java8Lexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = Java8Parser(stream)

        tree = parser.compilationUnit()
        print(ErrorListener.error)
        printer = KeyPrinter()
        walker = ParseTreeWalker()
        walker.walk(printer, tree)
        # print ("Tree " + tree.toStringTree(recog=parser))
        self.traverse(tree, parser.ruleNames)
        # print(tree.toStringTree(parser.ruleNames))

    def traverse(self,tree, rule_names, indent = 0):
        if tree.getText() == "<EOF>":
            return
        elif isinstance(tree, TerminalNodeImpl):
            token = tree.getSymbol()
            print("{0}TOKEN='{1}'".format("  " * indent, token.text))
            # print(rule_names[token.type])
            # print(str(token.line)+" "+str(token.column))
            # print(str.getInputStream())
            # print(tree.getSymbol().tokenIndex)
        else:
            print("{0}{1}".format("  " * indent, rule_names[tree.getRuleIndex()]))
            for child in tree.children:
                self.traverse(child, rule_names, indent + 1)

    def _on_click(self):
        self.tree.clear()
        self.main()


if __name__ == '__main__':

    app = QApplication([])

    window = Main()
    window.show()

    app.exec()