import sys
from antlr4 import *
from antlr4.tree.Tree import TerminalNodeImpl

from Java8Lexer import Java8Lexer
from Java8Parser import Java8Parser


def main(argv):
    input_stream = FileStream("C:\Javalib\example.java")
    lexer = Java8Lexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = Java8Parser(stream)
    tree = parser.compilationUnit()
    print(tree.getChildren(predicate=parser))
    # traverse(tree, parser.ruleNames)

def traverse(tree, rule_names, indent = 0):
    if tree.getText() == "<EOF>":
        return
    elif isinstance(tree, TerminalNodeImpl):
        token = tree.getSymbol()
        print("{0}TOKEN='{1}'".format("  " * indent, token.text))
        # print(rule_names[token.type])
        # print(str(token.line)+" "+str(token.column))
        # print(str.getInputStream())
        print(tree.getSymbol().tokenIndex)
    else:
        # print("{0}{1}".format("  " * indent, rule_names[tree.getRuleIndex()]))
        for child in tree.children:
            traverse(child, rule_names, indent + 1)

if __name__ == '__main__':
    main("C:\Javalib\example.java")