import sys
import traceback

from PyQt5.Qsci import QsciScintilla
from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QPushButton, \
     QMessageBox, QStyleFactory, QHBoxLayout, QTabWidget
from antlr4 import *
from antlr4.error import ErrorListener
from antlr4.tree.Tree import TerminalNodeImpl

from Java8Lexer import Java8Lexer
from Java8Parser import Java8Parser
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
        self.setStyleSheet('color: #191970')
        self.setStyle(QStyleFactory.create(QStyleFactory.keys()[0]))
        self.resize(800, 600)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel('')
        # self.tree.setHeaderLabels(['',''])

        self.tokens = QTreeWidget()
        self.tokens.setHeaderLabels(['Токен','Позиция','Тип'])
        self.tokens.setAlternatingRowColors(True)

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

        self.__lyt = QVBoxLayout()
        self.__myFont = QFont()
        self.__myFont.setPointSize(14)

        self.__tabMaster = TabMaster()
        self.__tabMaster.show_file(globals_.projectMainFile)
        self.__lyt.addWidget(self.__tabMaster)

        layout_H.addLayout(self.__lyt)
        layout.addLayout(layout_H)
        layout.addWidget(self.error)
        layout.addWidget(self.bp)

        self.last_line, self.last_index, self.last_size = None, None, None

        self.error_tree = []

        self.setLayout(layout)

    def parser_and_lexer(self):
        with open(globals_.projectMainFile, 'w') as file: file.writelines(tab_[0].text())
        input_stream = FileStream("C:\Javalib\example.java")

        lexer = Java8Lexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = Java8Parser(stream)
        tree = parser.compilationUnit()
        # print(len(tree.toStringTree(recog=parser).split(" ")))

        print ("Tree " + tree.toStringTree(recog=parser))
        print(tree.getTokens(63))

        self.tokensq(tree, parser.symbolicNames)

        if (len(ErrorListener.error) == 0) and (len(self.error_tree) == 0):
            Qw = QTreeWidgetItem(["Tree"])
            Qw.setForeground(0, QBrush(QColor(165, 60, 0)))

            self.tree.addTopLevelItem(Qw)

            self.traverse(tree, parser.ruleNames,Qw)
        else:
            print(self.error_tree)
            font = QFont("", 14)
            tree_err = QTreeWidgetItem(["Ошибка построения дерева."])
            tree_err.setFont(0, font)
            tree_err.setForeground(0,QBrush(QColor(220, 20, 60)))
            self.tree.addTopLevelItem(tree_err)
            if len(self.error_tree) != 0:
                for er in self.error_tree:
                    tmp_err = QTreeWidgetItem([er])
                    tmp_err.setForeground(0, QBrush(QColor(220, 20, 60)))
                    self.error.addTopLevelItem(tmp_err)
                    break
            else:
                for e in ErrorListener.error:
                    tmp_err = QTreeWidgetItem([e])
                    tmp_err.setForeground(0,QBrush(QColor(220, 20, 60)))
                    self.error.addTopLevelItem(tmp_err)

        self.tokens.clicked.connect(self._on_clik_token)

        # print(tree.toStringTree(parser.ruleNames))

    def tokensq(self, tree, symbolicNames):
        if tree.getText() == "<EOF>":
            return
        elif isinstance(tree, TerminalNodeImpl):
            token = tree.getSymbol()
            # print(token.text)
            if token.text == '/*':
                self.error_tree.append("Незакрытый комментарий на строке " + str(token.line) + ':' +str(token.column))

            if token.text == '\'':
                self.error_tree.append("Незакрытая кавычка \' на строке " + str(token.line) + ':' +str(token.column))

            if token.text == '\"':
                self.error_tree.append("Незакрытая кавычка \" на строке " + str(token.line) + ':' +str(token.column))

            tmp_token = QTreeWidgetItem([token.text, str(token.line) +":" + str(token.column), symbolicNames[token.type]])
            tmp_token.setForeground(0, QBrush(QColor(4, 54, 236)))
            tmp_token.setForeground(1, QBrush(QColor(4, 54, 236)))
            tmp_token.setForeground(2, QBrush(QColor(4, 54, 236)))
            self.tokens.addTopLevelItem(tmp_token)
        else:
            try:
                for child in tree.children:
                     self.tokensq(child, symbolicNames)
            except Exception as e:
                print(e)

    def traverse(self, tree, ruleNames, Qw, indent = 0):

        if tree.getText() == "<EOF>":
            return
        elif isinstance(tree, TerminalNodeImpl):
            print("{0}TOKEN='{1}'".format("  " * indent, tree.getSymbol().text))
            if tree.getSymbol().text == ';':
                print(tree.getSymbol())
                return
            if tree.getSymbol().text == '}':
                return
            if tree.getSymbol().text == '{':
                return
            if tree.getSymbol().text == ')':
                return
            if tree.getSymbol().text == '(':
                return
            if tree.getSymbol().text == '[':
                return
            if tree.getSymbol().text == ']':
                return
            tmp_tree = QTreeWidgetItem([tree.getText()])
            tmp_tree.setForeground(0, QBrush(QColor(172, 132, 0)))
            Qw.addChild(tmp_tree)
        else:
            # tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
            # tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
            # Qw.addChild(tmp_tree)
            if ruleNames[tree.getRuleIndex()] == 'literal':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'additiveExpression':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'multiplicativeExpression':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'classBodyDeclaration':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'classBody':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'assignmentOperator':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'variableDeclaratorId':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'packageDeclaration':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'packageName':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'classModifier':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'classDeclaration':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'unannType':
                tmp_tree = QTreeWidgetItem(['type'])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'methodModifier':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'methodHeader':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'methodDeclarator':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'methodDeclaration':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'formalParameterList':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'methodBody':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            elif ruleNames[tree.getRuleIndex()] == 'statement':
                tmp_tree = QTreeWidgetItem([ruleNames[tree.getRuleIndex()]])
                tmp_tree.setForeground(0, QBrush(QColor(59, 148, 15)))
                Qw.addChild(tmp_tree)
            else:
                tmp_tree = Qw


            print("{0}{1}".format("  " * indent, ruleNames[tree.getRuleIndex()]))


            for child in tree.children:
                self.traverse(child, ruleNames, tmp_tree, indent + 1)

    def _on_clik_token(self):
        getSelected = self.tokens.selectedItems()
        if getSelected:
            baseNode = getSelected[0]
            print(baseNode.text(0) + " " + baseNode.text(1) + " " +baseNode.text(2))

            line, index =  baseNode.text(1).split(":")
            tab_[0].indicatorDefine(QsciScintilla.FullBoxIndicator, 5)

            if self.last_line != None:
                tab_[0].clearIndicatorRange(self.last_line-1, self.last_index, self.last_line-1, self.last_index+self.last_size, 5)

            tab_[0].fillIndicatorRange(int(line)-1, int(index), int(line)-1, int(index)+int(len(baseNode.text(0))), 5)
            self.last_line, self.last_index, self.last_size = int(line), int(index), int(len(baseNode.text(0)))



    def _on_click(self):
        self.tree.clear()
        self.tokens.clear()
        self.error.clear()
        self.error_tree.clear()
        ErrorListener.error.clear()

        self.parser_and_lexer()



if __name__ == '__main__':

    app = QApplication([])

    window = Main()
    window.show()

    app.exec()