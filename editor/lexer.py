from PyQt5.QtGui import *
from PyQt5.Qsci import *
import re
from .ctags_parser import Ctags_parser

class MyLexer(QsciLexerCustom):

    def __init__(self, parent):
        super(MyLexer, self).__init__(parent)

        # Default text settings
        # ----------------------
        self.setDefaultColor(QColor("#ff000000"))
        self.setDefaultPaper(QColor("#ffffffff"))
        self.setDefaultFont(QFont("Consolas", 14))

        # Initialize colors per style
        # ----------------------------
        self.setColor(QColor("#ff" + "000000"), 0)  # black
        self.setColor(QColor("#ff" + "000000"), 1)  # black <b>
        self.setColor(QColor("#ff" + "d60404"), 2)  # red
        self.setColor(QColor("#ff" + "d60404"), 3)  # red <b>
        self.setColor(QColor("#ff" + "ff7f00"), 4)  # orange
        self.setColor(QColor("#ff" + "ff7f00"), 5)  # orange <b>
        self.setColor(QColor("#ff" + "ba9b00"), 6)  # yellow
        self.setColor(QColor("#ff" + "ba9b00"), 7)  # yellow <b>
        self.setColor(QColor("#ff" + "20ad20"), 8)  # lightgreen
        self.setColor(QColor("#ff" + "20ad20"), 9)  # lightgreen <b>
        self.setColor(QColor("#ff" + "005900"), 10)  # green
        self.setColor(QColor("#ff" + "005900"), 11)  # green <b>
        self.setColor(QColor("#ff" + "0202ce"), 12)  # blue
        self.setColor(QColor("#ff" + "0202ce"), 13)  # blue <b>
        self.setColor(QColor("#ff" + "9400d3"), 14)  # lightpurple
        self.setColor(QColor("#ff" + "9400d3"), 15)  # lightpurple <b>
        self.setColor(QColor("#ff" + "4b0082"), 16)  # purple
        self.setColor(QColor("#ff" + "4b0082"), 17)  # purple <b>
        self.setColor(QColor("#ff" + "0668d1"), 18)  # cyan
        self.setColor(QColor("#ff" + "0668d1"), 19)  # cyan <b>

        # Initialize paper colors per style
        # ----------------------------------
        self.setPaper(QColor("#ffffffff"), 0)  # white
        self.setPaper(QColor("#ffffffff"), 1)  # white
        self.setPaper(QColor("#ffffffff"), 2)  # white
        self.setPaper(QColor("#ffffffff"), 3)  # white
        self.setPaper(QColor("#ffffffff"), 4)  # white
        self.setPaper(QColor("#ffffffff"), 5)  # white
        self.setPaper(QColor("#ffffffff"), 6)  # white
        self.setPaper(QColor("#ffffffff"), 7)  # white
        self.setPaper(QColor("#ffffffff"), 8)  # white
        self.setPaper(QColor("#ffffffff"), 9)  # white
        self.setPaper(QColor("#ffffffff"), 10)  # white
        self.setPaper(QColor("#ffffffff"), 11)  # white
        self.setPaper(QColor("#ffffffff"), 12)  # white
        self.setPaper(QColor("#ffffffff"), 13)  # white
        self.setPaper(QColor("#ffffffff"), 14)  # white
        self.setPaper(QColor("#ffffffff"), 15)  # white
        self.setPaper(QColor("#ffffffff"), 16)  # white
        self.setPaper(QColor("#ffffffff"), 17)  # white
        self.setPaper(QColor("#ffffffff"), 18)  # white
        self.setPaper(QColor("#ffffffff"), 19)  # white

        # Initialize fonts per style
        # ---------------------------
        self.setFont(QFont("Consolas", 13, ), 0)
        self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 1)
        self.setFont(QFont("Consolas", 13, ), 2)
        self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 3)
        self.setFont(QFont("Consolas", 13, ), 4)
        self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 5)
        self.setFont(QFont("Consolas", 13, ), 6)
        self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 7)
        self.setFont(QFont("Consolas", 13, ), 8)
        self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 9)
        self.setFont(QFont("Consolas", 13, ), 10)
        self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 11)
        self.setFont(QFont("Consolas", 13, ), 12)
        self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 13)
        self.setFont(QFont("Consolas", 13, ), 14)
        self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 15)
        self.setFont(QFont("Consolas", 13, ), 16)
        self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 17)
        self.setFont(QFont("Consolas", 13, ), 18)
        self.setFont(QFont("Consolas", 13, weight=QFont.Bold), 19)

        # Access ctags parser
        # --------------------
        self.parser = Ctags_parser.Instance()

        # Indicator look and feel
        # ------------------------
        self.parent().indicatorDefine(QsciScintilla.HiddenIndicator, 0)
        self.parent().setIndicatorHoverStyle(QsciScintilla.PlainIndicator, 0)

    ''''''

    def language(self):
        return "SimpleLanguage"

    ''''''

    def description(self, style):
        if style == 0:
            return "black"
        elif style == 1:
            return "black <b>"
        elif style == 2:
            return "red"
        elif style == 3:
            return "red <b>"
        elif style == 4:
            return "orange"
        elif style == 5:
            return "orange <b>"
        elif style == 6:
            return "yellow"
        elif style == 7:
            return "yellow <b>"
        elif style == 8:
            return "lightgreen"
        elif style == 9:
            return "lightgreen <b>"
        elif style == 10:
            return "green"
        elif style == 11:
            return "green <b>"
        elif style == 12:
            return "blue"
        elif style == 13:
            return "blue <b>"
        elif style == 14:
            return "lightpurple"
        elif style == 15:
            return "lightpurple <b>"
        elif style == 16:
            return "purple"
        elif style == 17:
            return "purple <b>"
        elif style == 18:
            return "cyan"
        elif style == 19:
            return "cyan <b>"
        ###
        return ""

    ''''''

    def styleText(self, start, end):
        # 1. Initialize the styling procedure
        # ------------------------------------
        counter = start
        self.startStyling(start)

        # 2. Slice out a part from the text
        # ----------------------------------
        text = self.parent().text()[start:end]

        # 3. Tokenize the text
        # ---------------------
        p = re.compile(r"[*]\/|\/[*]|\s+|\w+|\W")

        # 'token_list' is a list of tuples: (token_name, token_len)
        token_list = [(token, len(bytearray(token, "utf-8"))) for token in p.findall(text)]

        # 4. Style the text
        # ------------------
        # 4.1 Check if multiline comment
        multiline_comm_flag = False
        editor = self.parent()
        if start > 0:
            previous_style_nr = editor.SendScintilla(editor.SCI_GETSTYLEAT, start - 1)
            if previous_style_nr == 11:
                multiline_comm_flag = True
            ###
        ###
        # 4.2 Style the text in a loop
        for i, token in enumerate(token_list):
            if multiline_comm_flag:
                # lightgreen
                self.setStyling(token[1], 8)
                if token[0] == "*/":
                    multiline_comm_flag = False
                ###
            ###
            else:
                if token[0] in ["(", ")", "{", "}", "[", "]"]:
                    # blue <b>
                    self.setStyling(token[1], 13)

                elif token[0] in ["signed", "unsigned", "char", "short", "int",
                                  "long", "bool", "float", "double", "void",
                                  "byte", "word", "dword",
                                  "int8_t", "uint8_t", "int16_t", "uint16_t",
                                  "int32_t", "uint32_t", "int64_t", "uint64_t"
                                  "int8", "uint8", "int16", "uint16",
                                  "int32", "uint32", "int64", "uint64"]:
                    # cyan
                    self.setStyling(token[1], 18)

                elif token[0] in ["#", "include"]:
                    # red
                    self.setStyling(token[1], 2)

                elif token[0] == "/*":
                    # lightgreen
                    multiline_comm_flag = True
                    self.setStyling(token[1], 8)

                else:
                    symbol_name, symbol_kind = self.parser.get_symbol_kind(token[0])

                    if symbol_kind == "":
                        if symbol_name != "":
                            # Default style <b>
                            self.setStyling(token[1], 7)
                        else:
                            # Default style
                            self.setStyling(token[1], 0)

                    elif symbol_kind in ["member"]:
                        # red
                        self.setStyling(token[1], 2)
                        editor.SendScintilla(QsciScintilla.SCI_SETINDICATORCURRENT, 0)
                        editor.SendScintilla(QsciScintilla.SCI_SETINDICATORVALUE, 0)
                        editor.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, counter, token[1])

                    elif symbol_kind in ["typedef", "macro", "enumerator", "label"]:
                        # blue
                        self.setStyling(token[1], 12)
                        editor.SendScintilla(QsciScintilla.SCI_SETINDICATORCURRENT, 0)
                        editor.SendScintilla(QsciScintilla.SCI_SETINDICATORVALUE, 0)
                        editor.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, counter, token[1])

                    elif symbol_kind in ["function"]:
                        # purple
                        self.setStyling(token[1], 16)
                        editor.SendScintilla(QsciScintilla.SCI_SETINDICATORCURRENT, 0)
                        editor.SendScintilla(QsciScintilla.SCI_SETINDICATORVALUE, 0)
                        editor.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, counter, token[1])

                    elif symbol_kind in ["variable", "local"]:
                        # green
                        self.setStyling(token[1], 10)
                        editor.SendScintilla(QsciScintilla.SCI_SETINDICATORCURRENT, 0)
                        editor.SendScintilla(QsciScintilla.SCI_SETINDICATORVALUE, 0)
                        editor.SendScintilla(QsciScintilla.SCI_INDICATORFILLRANGE, counter, token[1])

                    else:
                        # Default style
                        self.setStyling(token[1], 7)
                ###
            ###
            counter += token[1]
        ###

    ''''''


'''=== end Class ==='''