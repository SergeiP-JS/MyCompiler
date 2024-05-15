import sys
import builtins
import traceback

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

from editor import globals_
from editor.tiny_ide import TabMaster, tab_

def log_uncaught_exceptions(ex_cls, ex, tb):
    text = '{}: {}:\n'.format(ex_cls.__name__, ex)
    text += ''.join(traceback.format_tb(tb))

    print(text)
    QMessageBox.critical(None, 'Error', text)
    sys.exit(1)


sys.excepthook = log_uncaught_exceptions
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
        # self.error.setFixedHeight(100)


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




        # self.__editor = QsciScintilla()
        # self.__editor.setText("Hello\n")
        # self.__editor.append("worldыыыы")
        #
        # self.__editor.setLexer(None)
        # # self.__editor.setUtf8(True)  # Set encoding to UTF-8
        # self.__myFont = QFont()
        # self.__myFont.setPointSize(14)
        # self.__editor.setFont(self.__myFont)  # Will be overridden by lexer!

        self.__lyt = QVBoxLayout()
        self.__myFont = QFont()
        self.__myFont.setPointSize(14)

        # # 3. Place a button
        # # ------------------
        # self.__btn = QPushButton("Qsci")
        # self.__btn.setFixedWidth(50)
        # self.__btn.setFixedHeight(50)
        # self.__btn.clicked.connect(self.__btn_action)
        # self.__btn.setFont(self.__myFont)
        # self.__lyt.addWidget(self.__btn)

        # 4. Insert the TabMaster
        # ------------------------
        self.__tabMaster = TabMaster()
        self.__tabMaster.show_file(globals_.projectMainFile)
        self.__lyt.addWidget(self.__tabMaster)

        # # layout_H.addWidget(code)
        # layout_H.addWidget(self.__editor)
        layout_H.addLayout(self.__lyt)
        layout.addLayout(layout_H)
        layout.addWidget(self.error)
        layout.addWidget(self.bp)


        self.setLayout(layout)

    def __btn_action(self):
        print("Hello World")
        print(tab_[0].text())
        tab_[0].setText("sd")
    ''''''



    def parser_and_lexer(self):# argv
        # print(tab_[0].text())
        with open(globals_.projectMainFile, 'w') as file: file.writelines(tab_[0].text())
        # input_stream = FileStream(globals_.projectMainFile)
        input_stream = FileStream("C:\Javalib\example.java")
        # print(input_stream)
        lexer = Java8Lexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = Java8Parser(stream)

        tree = parser.compilationUnit()
        # print(ErrorListener.error)
        # printer = KeyPrinter()


        # walker = ParseTreeWalker()
        # walker.walk(printer, tree)
        # print ("Tree " + tree.toStringTree(recog=parser))
        print(len(ErrorListener.error))
        # if len(ErrorListener.error) == 0:
        self.traverse(tree, parser.ruleNames)
        # else:
        #     for e in ErrorListener.error:
        #         self.error.addTopLevelItem(QTreeWidgetItem([e]))
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
        self.tokens.clear()
        self.error.clear()
        ErrorListener.error.clear()

        val = QTreeWidgetItem(['1'])

        val2=QTreeWidgetItem([ '2'])

        children=[QTreeWidgetItem(['', 'equals1']),QTreeWidgetItem(['', 'equals1'])]
        children.append(QTreeWidgetItem(['', 'equals1']))

        val2.addChildren(children)
        val.addChild(val2)

        self.tree.addTopLevelItem(val)
        self.parser_and_lexer()



if __name__ == '__main__':

    app = QApplication([])

    window = Main()
    window.show()

    app.exec()