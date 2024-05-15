import sys
import builtins
import traceback

from PyQt5.Qsci import QsciScintilla
from PyQt5.QtGui import QFont, QBrush, QColor
from antlr4 import *
from antlr4.error import ErrorListener
from antlr4.tree.Tree import TerminalNodeImpl




# import MyErrorListener
from Java8Lexer import Java8Lexer
from Java8Parser import Java8Parser
# from Java8ParserListener import *

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QPushButton, \
    QProgressDialog, QMessageBox, QStyleFactory, QHBoxLayout, QTabWidget, QLineEdit, QTextEdit, QAbstractScrollArea, \
    QHeaderView
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
        # self.setFixedSize(800, 480)
        # self.setMinimumSize(1280, 960)
        self.setStyleSheet('color: #191970')
        self.setStyle(QStyleFactory.create(QStyleFactory.keys()[0]))
        self.resize(800, 600)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(['',''])
        # self.tree.horizontalScrollBarPolicy()
        # self.tre
        # self.tree.horizontalScrollBar().setEnabled(True)

        self.tokens = QTreeWidget()
        self.tokens.setHeaderLabels(['Токен','Позиция','Тип'])
        self.tokens.setAlternatingRowColors(True)
        # self.tokens.setStyleSheet("background-color: green; color: white")

        self.tab = QTabWidget()
        self.tab.addTab(self.tokens, "Токены")
        self.tab.addTab(self.tree, "Дерево")

        self.error = QTreeWidget()
        self.error.setFixedHeight(150)
        self.error.setHeaderLabel('Ошибки')
        self.error.setFont(font)


        self.bp = QPushButton('Получить токены и построить дерево')
        self.bp.clicked.connect(self._on_click)
        self.bp.setStyleSheet("background-color: rgba(4, 54, 236, 0.625); color: #FFEFD5")
        self.bp.setFont(font)

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

        self.last_line, self.last_index, self.last_size = None, None, None

        self.setLayout(layout)

    # def __btn_action(self):
    #     print("Hello World")
    #     print(tab_[0].text())
    #     tab_[0].setText("sd")
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
        #
        #
        # walker = ParseTreeWalker()
        # walker.walk(printer, tree)
        # print ("Tree " + tree.toStringTree(recog=parser))
        # print(len(ErrorListener.error))
        # print(tree.children)

        if len(ErrorListener.error) == 0:
            Qw = QTreeWidgetItem(["Tree"])
            Qw.setForeground(0, QBrush(QColor(165, 60, 0)))
            self.tree.addTopLevelItem(Qw)
            self.traverse(tree, parser.ruleNames,Qw)
            self.tokens.clicked.connect(self._on_clik_token)
        else:
            self.tokensq(tree, parser.ruleNames)
            self.tokens.clicked.connect(self._on_clik_token)

            font = QFont("", 14)
            tree_err=QTreeWidgetItem(["Ошибка построения дерева."])
            # tree_err.setBackground(0,QBrush(QColor("blue")))
            tree_err.setFont(0, font)
            tree_err.setForeground(0,QBrush(QColor(220, 20, 60)))
            self.tree.addTopLevelItem(tree_err)

            for e in ErrorListener.error:
                tmp_err = QTreeWidgetItem([e])
                tmp_err.setForeground(0,QBrush(QColor(220, 20, 60)))
                self.error.addTopLevelItem(tmp_err)

        print(tree.toStringTree(parser.ruleNames))
        # self.tokensq(tree,parser.ruleNames)

    def tokensq(self, tree, rule_names):
        if tree.getText() == "<EOF>":
            return
        elif isinstance(tree, TerminalNodeImpl):
            # print()
            token = tree.getSymbol()
            # print(rule_names[token.type])
            # print(str(token.line)+" "+str(token.column))
            print(token.text)

            tmp_token = QTreeWidgetItem([token.text,str(token.line)+":"+str(token.column),rule_names[token.type]])
            tmp_token.setForeground(0, QBrush(QColor(4, 54, 236)))
            tmp_token.setForeground(1, QBrush(QColor(4, 54, 236)))
            #  459abf
            tmp_token.setForeground(2, QBrush(QColor(4, 54, 236)))
            self.tokens.addTopLevelItem(tmp_token)
        else:
            try:
                for child in tree.children:
                    # print(tree.children)
                     self.tokensq(child, rule_names)
            except Exception as e:
                print(e)

    def traverse(self,tree, rule_names,Qw, indent = 0):

        if tree.getText() == "<EOF>":
            return
        elif isinstance(tree, TerminalNodeImpl):
            token = tree.getSymbol()
            # print(rule_names[token.type])
            # # print(str(token.line)+" "+str(token.column))
            # print(token.text)
            print("{0}TOKEN='{1}'".format("  " * indent, tree.getText()))

            tmp_token = QTreeWidgetItem([token.text, str(token.line) + ":" + str(token.column), rule_names[token.type]])
            tmp_token.setForeground(0, QBrush(QColor(4, 54, 236)))
            tmp_token.setForeground(1, QBrush(QColor(4, 54, 236)))
            #  459abf
            tmp_token.setForeground(2, QBrush(QColor(4, 54, 236)))

            tmp_tree = QTreeWidgetItem(["TOKEN='{0}'".format(tree.getText())])
            tmp_tree.setForeground(0, QBrush(QColor(172, 132, 0)))
            Qw.addChild(tmp_tree)
            self.tokens.addTopLevelItem(tmp_token)
        else:
            tmp_tree = QTreeWidgetItem([rule_names[tree.getRuleIndex()]])
            tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
            Qw.addChild(tmp_tree)
            print("{0}{1}".format("  " * indent, rule_names[tree.getRuleIndex()]))
            for child in tree.children:

                # self.tree.addTopLevelItem(tmp_tree)
                self.traverse(child, rule_names,tmp_tree, indent + 1)

    def _on_clik_token(self):
        getSelected = self.tokens.selectedItems()
        if getSelected:
            baseNode = getSelected[0]
            getChildNode = baseNode.text(1)
            # print(len(baseNode.text(0)))
            print(baseNode.text(0) + " " + baseNode.text(1) + " " +baseNode.text(2))

            line, index =  baseNode.text(1).split(":")

            # print(tab_[0].getCursorPosition())
            tab_[0].indicatorDefine(QsciScintilla.FullBoxIndicator, 5)

            if self.last_line != None:
                tab_[0].clearIndicatorRange(self.last_line-1, self.last_index, self.last_line-1, self.last_index+self.last_size, 5)

            tab_[0].fillIndicatorRange(int(line)-1, int(index), int(line)-1, int(index)+int(len(baseNode.text(0))), 5)
            self.last_line, self.last_index, self.last_size = int(line), int(index), int(len(baseNode.text(0)))



    def _on_click(self):
        self.tree.clear()
        self.tokens.clear()
        self.error.clear()
        ErrorListener.error.clear()




        # val = QTreeWidgetItem(['1'])
        #
        # val2=QTreeWidgetItem([ '2'])
        #
        # children=[QTreeWidgetItem(['', 'equals1']),QTreeWidgetItem(['', 'equals1'])]
        # children.append(QTreeWidgetItem(['', 'equals1']))
        #
        # val2.addChildren(children)
        # val.addChild(val2)

        # self.tree.addTopLevelItem(val)
        self.parser_and_lexer()



if __name__ == '__main__':

    app = QApplication([])

    window = Main()
    window.show()

    app.exec()